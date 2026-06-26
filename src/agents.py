from langchain_openai import ChatOpenAI
from src.tools import get_search_tool
from src.schemas import PlannerOutput, ReflectorOutput
from dotenv import load_dotenv
import ast

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


def searcher_node(state):
    sub_queries = state["sub_queries"]
    all_results = []

    for query in sub_queries:
        response = search_tool.invoke({"query": query})
        results = response["results"]
        for r in results:
            all_results.append(f"Source: {r['url']}\n{r['content']}")

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