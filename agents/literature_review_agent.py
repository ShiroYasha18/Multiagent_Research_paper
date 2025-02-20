import requests
import datetime
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module

class LiteratureReviewAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message=(
                "You are a research assistant specializing in academic literature reviews. "
                "Your task is to extract key findings, identify research gaps, and summarize insights "
                "STRICTLY from the provided research papers. "
                "DO NOT generate information beyond the provided sources. "
                "Always ensure APA-style citations for every referenced work."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def fetch_research_papers(self, query, max_results=10):
        """Fetches recent (last 10 years) research papers from ArXiv."""
        base_url = "http://export.arxiv.org/api/query"
        current_year = datetime.datetime.now().year
        min_year = current_year - 10
        params = {
            "search_query": f"all:{query} AND submittedDate:[{min_year}0000 TO {current_year}9999]",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        response = requests.get(base_url, params=params)
        papers = []

        if response.status_code == 200:
            entries = response.text.split("<entry>")[1:]
            for entry in entries:
                title = entry.split("<title>")[1].split("</title>")[0].strip()
                summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
                link = entry.split("<id>")[1].split("</id>")[0].strip()
                papers.append(f"**{title}**\nSummary: {summary}\nSource: {link}")

        return papers if papers else ["No relevant research papers found."]

    def review_literature(self, topic):
        """Fetch and analyze relevant research papers with improved focus on accuracy."""
        research_papers = self.fetch_research_papers(topic)

        # Check if valid research papers were found
        if len(research_papers) == 1 and "No relevant research papers found." in research_papers:
            return "❌ No relevant research papers found in the last 10 years for this topic. Consider refining the query.", []

        research_text = "\n\n".join(research_papers[:10])  # Limit input size

        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=(
                f"Review the following research papers on **{topic}**. "
                "Your task is to summarize key findings, identify research gaps, and cite sources in APA format. "
                "Ensure your response is STRICTLY based on the provided content. Do NOT fabricate citations.\n\n"
                f"{research_text}\n\n"
                "**Instructions:**\n"
                "- Extract key findings without adding personal opinions.\n"
                "- Clearly highlight at least 2-3 research gaps based on the findings.\n"
                "- List all references properly in APA format.\n"
            )
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to generate a summary. Try again.", []

        return response.msgs[0].content, research_papers  # Return structured summary & references
