# hypothesis_generation_agent.py

from camel.agents import ChatAgent
from tools.memory_module import create_memory_module
from camel.messages import BaseMessage
from camel.types import RoleType  # ✅ Import RoleType


class HypothesisGenerationAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message="You generate precise, measurable scientific hypotheses with independent & dependent variables.",
            model=model,
            memory=create_memory_module(),
        )

    def generate_hypothesis(self, research_summary):
        """Generate a well-defined, measurable hypothesis based on the literature review."""
        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=f"Based on the following research summary, create a precise hypothesis with measurable variables:\n\n{research_summary}"
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to generate a hypothesis. Try again."

        return response.msgs[0].content  # Return refined hypothesis