import requests
import re
import numpy as np
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module


class DataAnalysisAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message=(
                "You are an AI research data analyst. "
                "Your role is to extract numerical results from research papers, "
                "compare findings across multiple sources, detect inconsistencies, "
                "and highlight potential research gaps. \n\n"
                "**Guidelines:**\n"
                "- Extract numerical data accurately from summaries.\n"
                "- Identify inconsistencies using statistical methods (variance, standard deviation).\n"
                "- Highlight gaps in methodology or data quality.\n"
                "- Provide structured, well-formatted insights."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def fetch_paper_results(self, query, max_results=5):
        """
        Fetches research papers related to the given query and extracts numerical findings.
        Uses ArXiv as the primary source.
        """
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

                # ✅ Extract numerical values using regex
                numbers = re.findall(r'\b\d+\.?\d*\b', summary)
                numbers = [float(num) for num in numbers]

                research_results.append({"title": title, "values": numbers, "link": link})

        return research_results  # ✅ Returns structured data

    def compare_research_findings(self, topic):
        """
        Compares numerical results from multiple research papers to identify inconsistencies.
        Uses statistical analysis to detect research gaps.
        """
        research_results = self.fetch_paper_results(topic)

        if not research_results or not isinstance(research_results, list):
            return "❌ No numerical data available for comparison."

        # ✅ Filter valid papers that contain numerical values
        valid_papers = [paper for paper in research_results if isinstance(paper, dict) and "values" in paper and paper["values"]]

        if len(valid_papers) < 2:
            return "❌ Not enough valid research papers for numerical comparison."

        # ✅ Generate comparison insights
        comparison_text = "📊 **Research Findings Comparison:**\n"
        all_values = []

        for paper in valid_papers:
            comparison_text += f"- **{paper['title']}**: Values: {paper['values']} - [📄 Source]({paper['link']})\n"
            all_values.extend(paper["values"])

        # ✅ Perform statistical analysis
        mean_value = np.mean(all_values)
        std_dev = np.std(all_values)
        variance = np.var(all_values)

        comparison_text += f"\n📈 **Statistical Insights:**\n"
        comparison_text += f"- **Mean Reported Value:** {round(mean_value, 2)}\n"
        comparison_text += f"- **Standard Deviation:** {round(std_dev, 2)} (Lower means higher agreement)\n"
        comparison_text += f"- **Variance:** {round(variance, 2)} (Higher suggests inconsistency)\n"

        # ✅ Identify Research Gaps Based on Variability
        if std_dev > 10:  # ✅ Threshold for inconsistency detection
            comparison_text += "\n❗ **Potential Research Gaps Identified:**\n"

            # Methodology Gap: High variance suggests methodological differences
            if variance > 100:
                comparison_text += "- **Methodological Discrepancies:** Differences in experimental setup, dataset variations, or feature selection may be causing inconsistent results.\n"

            # Data Gap: Extreme outliers suggest possible data quality issues
            if max(all_values) / mean_value > 3:
                comparison_text += "- **Data Quality Concerns:** Some results deviate significantly, suggesting dataset biases or noise in specific studies.\n"

        return comparison_text
