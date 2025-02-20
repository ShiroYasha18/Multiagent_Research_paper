import os
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module
from dotenv import load_dotenv

# ✅ Load API Keys
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")


class ResearchWriter:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message="You are an AI research assistant that refines and formats research papers in an academic writing style.",
            model=model,
            memory=create_memory_module(),
        )
        self.conversation_history = []

    def refine_research(self, research_outputs):
        """Refines raw research outputs into well-structured research writing."""

        structured_prompt = f"""
        ✍ **Research Paper Refinement Task** ✍
        Given the following AI-generated research content:

        {research_outputs}

        ✅ **Your Task:**
        1. **Refine the writing style** to be **more professional and academic**.
        2. **Improve coherence and structure** to match a proper **research paper format**.
        3. **Add smooth transitions between sections** for better readability.
        4. **Ensure clarity, conciseness, and formal tone**.

        🎯 **Final Output Format:**
        - **Title:** Automatically generate a suitable research title.
        - **Abstract:** Summarize the key findings in 100-150 words.
        - **Introduction:** Provide background on the problem.
        - **Literature Review:** Summarize related research.
        - **Methodology:** Explain the AI experimental design.
        - **Results & Discussion:** Analyze AI testing performance.
        - **Conclusion:** Summarize key insights and future research directions.
        - **References:** Suggest sources (if available).

        📌 **Final Output Should Look Like a Real Research Paper.**
        """

        # ✅ Send structured request to AI model
        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=structured_prompt,
        )

        response = self.agent.step(user_message)

        # ✅ Save refined research
        refined_text = response.msgs[0].content
        self.conversation_history.append(refined_text)

        return refined_text
