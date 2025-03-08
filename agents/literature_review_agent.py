import os
import requests
from dotenv import load_dotenv
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module
from datetime import datetime

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

    def fetch_google_scholar_papers(self, query, max_results=5):
        """Fetches research papers from Google Scholar using SerpAPI."""
        if not SERPAPI_API_KEY:
            print("❌ SERPAPI_API_KEY is missing. Please add it to your .env file.")
            return []

        print("🔍 Searching Google Scholar for relevant research papers...")
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "engine": "google_scholar",
            "api_key": SERPAPI_API_KEY,
            "num": max_results
        }
        response = requests.get(url, params=params)
        papers = []

        if response.status_code == 200:
            results = response.json().get("organic_results", [])
            for result in results:
                title = result.get("title", "No title available")
                summary = result.get("snippet", "No summary available")
                link = result.get("link", "No link available")
                papers.append({"title": title, "summary": summary, "link": link})

        return papers if papers else []

    def review_literature(self, topic):
        """Fetch and analyze relevant research papers from ArXiv & Google Scholar."""

        print(f"\n🔍 Searching for research papers on: **{topic}**\n")

        arxiv_papers = self.fetch_arxiv_papers(topic)
        scholar_papers = self.fetch_google_scholar_papers(topic)

        all_papers = arxiv_papers + scholar_papers

        if not all_papers:
            print("❌ No relevant research papers found. Research canceled.")
            return "❌ No relevant research papers found.", [], []

        print(f"✅ Retrieved {len(all_papers)} papers:\n")
        for paper in all_papers:
            print(f"- {paper['title']} ({paper['link']})")

        research_text = "\n\n".join(
            [f"**{p['title']}**\nSummary: {p['summary']}\nSource: {p['link']}" for p in all_papers]
        )

        # ✅ Ensure research text isn't too long for LLM
        max_tokens = 4000
        if len(research_text) > max_tokens:
            print("⚠️ Research text too long. Truncating...")
            research_text = research_text[:max_tokens]

        print("\n📝 Passing the following text to ChatAgent:\n")
        print(research_text[:1000])  # ✅ Print first 1000 characters for debugging

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

        # ✅ Parse AI response for research summary & gaps
        response_text = response.msgs[0].content
        summary, gaps = self.extract_gaps_from_summary(response_text)

        # ✅ Attach research gap citations
        research_summary = summary + "\n\n📌 **Cited Papers for Research Gaps:**\n"
        for paper in all_papers:
            research_summary += f"- {paper['title']} (Source: {paper['link']})\n"

        return research_summary, all_papers, gaps  # ✅ Return summary, citations, and research gaps

    def extract_gaps_from_summary(self, text):
        """Extracts research gaps from the AI-generated summary."""
        research_gaps = []
        summary_sections = text.split("\n")

        capture = False
        gap_text = ""
        summary = ""

        for line in summary_sections:
            if "Research Gap" in line:  # ✅ Identifying research gaps
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

        if gap_text:  # ✅ Catch last research gap if missed
            research_gaps.append(gap_text.strip())

        return summary, research_gaps
