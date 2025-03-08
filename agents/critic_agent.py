from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module


class CriticAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message=(
                "You are a Critic Agent. Your task is to critically evaluate the hypothesis, identify logical flaws, and suggest improvements."
                "Additionally, engage in **Self-Reflection Loops** to recursively refine the critique until no further improvements are possible."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def critique_hypothesis(self, hypothesis):
        critique_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=f"Critique this hypothesis and suggest improvements: {hypothesis}."
        )

        response = self.agent.step(critique_message)
        if not response.msgs or not response.msgs[0].content.strip():
            return "No Critique Generated."

        critique = response.msgs[0].content

        # Self-Reflection Loop
        for _ in range(3):  # Max 3 iterations
            reflection_message = BaseMessage(
                role_name="User",
                role_type=RoleType.USER,
                meta_dict={},
                content=f"Reflect on the following critique and suggest additional improvements: {critique}."
            )

            reflection_response = self.agent.step(reflection_message)
            if reflection_response.msgs and reflection_response.msgs[0].content.strip():
                critique += "\n\n**Self-Reflection:**\n" + reflection_response.msgs[0].content
            else:
                break

        return critique