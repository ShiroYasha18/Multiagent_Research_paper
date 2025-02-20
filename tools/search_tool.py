# tools/search_tool.py

from camel.toolkits import SearchToolkit, FunctionTool

def create_search_tool():
    search_toolkit = SearchToolkit()
    return FunctionTool(search_toolkit.tavily_search)
