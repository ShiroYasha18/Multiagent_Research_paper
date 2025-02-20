# critic_agent.py

from camel.agents import ChatAgent
from tools.memory_module import create_memory_module
from camel.messages import BaseMessage
from camel.types import RoleType  # ✅ Import RoleType

class CriticAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message="You are a critical reviewer. Your task is to find flaws in scientific hypotheses and suggest improvements.",
            model=model,
            memory=create_memory_module(),
        )
        self.conversation_history = []

    def critique_hypothesis(self, hypothesis):
        """Challenges a given hypothesis and suggests improvements."""

        max_input_length = 1000
        truncated_hypothesis = hypothesis[:max_input_length]

        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},  # ✅ FIX: Added meta_dict={}
            content=f"Critique this hypothesis and suggest improvements: {truncated_hypothesis}"
        )

        self.conversation_history.append(user_message)

        print("🧐 Critic Agent Message Sent:", user_message)

        response = self.agent.step(user_message)

        if not response.msgs:
            return "✅ No critical issues found. The hypothesis is already strong."

        self.conversation_history.append(response.msgs[0])

        return response.msgs[0].content
