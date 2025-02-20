import requests
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module
from semanticscholar import SemanticScholar


class DataAnalysisAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message="You are an AI data analyst. Your task is to analyze research findings and identify inconsistencies using statistical methods.",
            model=model,
            memory=create_memory_module(),
        )

    def analyze_results(self, research_results):
        """Compare research findings using statistical methods and highlight discrepancies."""
        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=f"Analyze the following research findings and identify inconsistencies. Use numerical comparisons and statistical models:\n\n{research_results}"
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to analyze data. Try again."

        return response.msgs[0].content
