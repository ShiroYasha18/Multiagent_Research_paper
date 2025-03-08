import os
import requests
from dotenv import load_dotenv
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType

from agents.dataextractionagent import DatasetExtractionAgent
dataset_agent = DatasetExtractionAgent()

from tools.memory_module import create_memory_module
from datetime import datetime
import numpy as np

# ✅ Load API Keys
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

class LiteratureReviewAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message=(
                "You are an advanced research assistant specializing in academic literature reviews. "
                "Your task is to retrieve, summarize, and critically analyze research papers STRICTLY based on provided sources. "
                "Ensure citations are in APA format. DO NOT generate any information beyond the given sources."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def fetch_arxiv_papers(self, query, max_results=10):
        """Fetches recent (last 10 years) research papers from ArXiv."""
        print("🔍 Searching ArXiv for relevant research papers...")
        base_url = "http://export.arxiv.org/api/query"
        current_year = datetime.now().year
        min_year = current_year - 10
        params = {
            "search_query": f"all:{query} AND submittedDate:[{min_year} TO {current_year}]",
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
                papers.append({"title": title, "summary": summary, "link": link})

        return papers if papers else []

    def evaluate_research_gaps(self, gaps):
        print("🔍 Calculating Research Gap Confidence Scores...")
        scored_gaps = []
        for gap in gaps:
            length_score = len(gap.split()) / 100  # Word count normalization
            novelty_score = np.random.uniform(0.6, 1.0)  # Simulated novelty score (0.6-1.0 range)
            confidence = round((0.7 * length_score) + (0.3 * novelty_score), 3)
            scored_gaps.append((gap, confidence))

        scored_gaps = sorted(scored_gaps, key=lambda x: x[1], reverse=True)
        return scored_gaps

    def review_literature(self, topic):
        """Fetch and analyze relevant research papers from ArXiv & Google Scholar."""

        print(f"\n🔍 Searching for research papers on: **{topic}**\n")

        arxiv_papers = self.fetch_arxiv_papers(topic)
        all_papers = arxiv_papers

        if not all_papers:
            print("❌ No relevant research papers found. Research canceled.")
            return "❌ No relevant research papers found.", [], []

        print(f"✅ Retrieved {len(all_papers)} papers:\n")
        for paper in all_papers:
            print(f"- {paper['title']} ({paper['link']})")

        research_text = "\n\n".join(
            [f"**{p['title']}**\nSummary: {p['summary']}\nSource: {p['link']}" for p in all_papers]
        )

        max_tokens = 4000
        if len(research_text) > max_tokens:
            print("⚠️ Research text too long. Truncating...")
            research_text = research_text[:max_tokens]

        print("\n📝 Passing the following text to ChatAgent:\n")
        print(research_text[:1000])

        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=(
                f"Summarize the findings of these research papers on **{topic}**. "
                "Strictly extract information from the given sources. "
                "Identify at least **3 key research gaps** and explain them in detail with citations.\n\n"
                "**Instructions:**\n"
                "- List key takeaways from each paper.\n"
                "- Clearly highlight at least 3 research gaps based on the findings.\n"
                "- Ensure all references are properly cited in APA format.\n"
                "- Do NOT generate extra details beyond the provided sources.\n\n"
                f"{research_text}"
            )
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to generate a summary. Try again.", [], []

        response_text = response.msgs[0].content
        summary, gaps = self.extract_gaps_from_summary(response_text)
        scored_gaps = self.evaluate_research_gaps(gaps)

        return summary, all_papers, scored_gaps

    def extract_gaps_from_summary(self, text):
        research_gaps = []
        summary_sections = text.split("\n")
        capture = False
        gap_text = ""
        summary = ""

        for line in summary_sections:
            if "Research Gap" in line:
                capture = True
                if gap_text:
                    research_gaps.append(gap_text.strip())
                    gap_text = line.strip()
                else:
                    gap_text = line.strip()
            elif capture:
                if line.strip() == "":
                    research_gaps.append(gap_text.strip())
                    gap_text = ""
                    capture = False
                else:
                    gap_text += " " + line.strip()
            else:
                summary += line + "\n"

        if gap_text:
            research_gaps.append(gap_text.strip())

        return summary, research_gaps
