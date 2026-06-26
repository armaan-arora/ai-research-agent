from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

def get_search_tool():
    search = TavilySearch(max_results=5)
    return search