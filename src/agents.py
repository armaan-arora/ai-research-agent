from langchain_openai import ChatOpenAI
from src.tools import get_search_tool
from src.schemas import PlannerOutput, ReflectorOutput
from dotenv import load_dotenv
import asyncio


from src.memory import store_results, retrieve_results, has_results

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
search_tool = get_search_tool()

llm_planner = llm.with_structured_output(PlannerOutput)
llm_reflector = llm.with_structured_output(ReflectorOutput)


def planner_node(state):
    topic = state["topic"]

    prompt = f"""You are a research planner.
Given this topic: {topic}
Generate exactly 3 focused search queries to research this topic thoroughly."""

    response = llm_planner.invoke(prompt)

    # response is now a PlannerOutput object, not text
    print(f"\nPlanner queries: {response.sub_queries}")
    return {"sub_queries": response.sub_queries}


async def search_single_query(query):
    # check RAG memory first
    if has_results(query):
        cached = retrieve_results(query)
        return cached
    
    #not in memory
    response = await asyncio.to_thread(search_tool.invoke, {"query": query})
    results = response["results"]
    formatted = [f"Source: {r['url']}\n{r['content']}" for r in results]
    # store in memory for next time
    store_results(query, formatted)

    return formatted

# def searcher_node(state):
#     sub_queries = state["sub_queries"]
#     all_results = []

#     for query in sub_queries:
#         response = search_tool.invoke({"query": query})
#         results = response["results"]
#         for r in results:
#             all_results.append(f"Source: {r['url']}\n{r['content']}")

#     return {"search_results": all_results}

def searcher_node(state):
    sub_queries = state["sub_queries"]

    async def run_all():
        tasks = [search_single_query(q) for q in sub_queries]
        results = await asyncio.gather(*tasks)
        return results

    all_nested = asyncio.run(run_all())
    
    # flatten list of lists into single list
    all_results = []
    for sublist in all_nested:      # loop through each query's results
        for item in sublist:        # loop through each result
            all_results.append(item)
    
    print(f"\nSearcher found {len(all_results)} results in parallel")
    return {"search_results": all_results}


def reflector_node(state):
    topic = state["topic"]
    search_results = "\n\n".join(state["search_results"])
    loop_count = state.get("loop_count", 0)

    prompt = f"""You are a research quality checker.

Topic: {topic}

Here are the current search results:
{search_results}

Analyze if there is enough information for a comprehensive report.
Identify any key gaps or missing aspects."""

    response = llm_reflector.invoke(prompt)

    # response is now a ReflectorOutput object
    print(f"\nReflector verdict: {response.verdict}")
    print(f"Gaps: {response.gaps}")

    return {
        "reflection_notes": response.gaps,
        "sub_queries": response.new_queries if response.new_queries else state["sub_queries"],
        "loop_count": loop_count + 1
    }


def reporter_node(state):
    topic = state["topic"]
    results = "\n\n".join(state["search_results"])

    prompt = f"""You are a research report writer.
Topic: {topic}

Here is the raw research data:
{results}

Write a clean, structured markdown report with:
- A title
- 3-4 key sections
- Bullet points for key facts
- Source URLs cited inline

Report:"""

    response = llm.invoke(prompt)
    return {"report": response.content}


def should_continue(state):
    loop_count = state.get("loop_count", 0)
    reflection_notes = state.get("reflection_notes", "")

    if loop_count >= 2:
        print("\nMax loops reached, generating report...")
        return "reporter"

    if reflection_notes.lower() == "none" or reflection_notes == "":
        print("\nSufficient info found, generating report...")
        return "reporter"

    print("\nGaps found, searching again...")
    return "searcher"