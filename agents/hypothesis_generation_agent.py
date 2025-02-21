from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module

class HypothesisGenerationAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message="You are a scientific researcher specializing in hypothesis formulation. "
                           "Your job is to generate a strong, testable hypothesis based on research findings and gaps. "
                           "Ensure logical coherence and real-world applicability.",
            model=model,
            memory=create_memory_module(),
        )

    def generate_hypothesis(self, review):
        """Generate a hypothesis based on literature review findings."""
        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=(
                "Based on the literature review findings, generate a clear, testable scientific hypothesis. "
                "Ensure the hypothesis is based on identified research gaps, uses logical reasoning, and is aligned with real-world applications.\n\n"
                f"**Literature Review Findings:**\n{review}\n\n"
                "**Guidelines:**\n"
                "- Clearly define the independent and dependent variables.\n"
                "- Ensure feasibility in experimental validation.\n"
                "- Justify why this hypothesis fills the identified research gaps."
            )
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to generate a hypothesis. Try again."

        return response.msgs[0].content
