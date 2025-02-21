import requests
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module


class DataAnalysisAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message=(
                "You are an AI research data analyst. "
                "Your task is to compare numerical results from research papers, "
                "detect inconsistencies, and highlight potential research gaps."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def fetch_paper_results(self, query, max_results=5):
        """Fetches numerical findings from research papers via ArXiv."""
        base_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }

        response = requests.get(base_url, params=params)
        research_results = []

        if response.status_code == 200:
            entries = response.text.split("<entry>")[1:]
            for entry in entries:
                title = entry.split("<title>")[1].split("</title>")[0].strip()
                summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
                link = entry.split("<id>")[1].split("</id>")[0].strip()

                # ✅ Extract numerical data from summary
                numbers = [float(num) for num in summary.split() if num.replace('.', '', 1).isdigit()]

                research_results.append({"title": title, "values": numbers, "link": link})

        return research_results  # ✅ Returns structured data

    def compare_research_findings(self, topic):
        """Compare numerical results from different research papers to find inconsistencies."""
        research_results = self.fetch_paper_results(topic)

        if not research_results or not isinstance(research_results, list):
            return "❌ No numerical data available for comparison."

        # ✅ Filter only valid papers that contain numerical values
        valid_papers = [paper for paper in research_results if isinstance(paper, dict) and "values" in paper and paper["values"]]

        if len(valid_papers) < 2:
            return "❌ Not enough valid research papers for numerical comparison."

        # ✅ Generate comparison insights
        comparison_text = "📊 **Research Comparison Across Papers:**\n"
        for paper in valid_papers:
            comparison_text += f"- **{paper['title']}**: Values: {paper['values']} - [Link]({paper['link']})\n"

        # ✅ Identify research gaps based on numerical inconsistencies
        max_value = max(max(p["values"]) for p in valid_papers)
        min_value = min(min(p["values"]) for p in valid_papers)
        difference = max_value - min_value

        if difference > 10:  # ✅ Threshold for inconsistency detection
            comparison_text += f"\n❗ **Potential Research Gap Identified:** The reported results range from {min_value} to {max_value}, suggesting inconsistency in findings.\n"

        return comparison_text
