from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module


class CriticAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message=(
                "You are an expert research critic. Your task is to analyze hypotheses and provide"
                " **constructive criticism** by identifying weaknesses and suggesting **precise improvements**.\n\n"
                "**Guidelines:**\n"
                "- Identify **logical inconsistencies, unclear assumptions, or testability issues**.\n"
                "- Ensure the hypothesis **aligns with the research gaps** and is scientifically rigorous.\n"
                "- Suggest **specific refinements** while maintaining testability.\n"
                "- If the hypothesis is strong, suggest ways to improve its clarity or validation approach.\n"
                "- Avoid rejecting the hypothesis entirely—focus on **enhancing it**."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def critique_hypothesis(self, hypothesis, research_gaps):
        """
        Critiques the given hypothesis and provides specific improvement suggestions.

        :param hypothesis: The hypothesis to critique.
        :param research_gaps: The identified research gaps.
        :return: A structured critique with actionable refinements.
        """

        if not hypothesis or "❌" in hypothesis:
            return "❌ No valid hypothesis to critique."

        if not research_gaps:
            return "❌ No research gaps provided for critique."

        formatted_gaps = "\n".join([f"- {gap}" for gap in research_gaps])

        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=(
                f"Analyze the following **hypothesis** and provide constructive critique "
                "by evaluating its **scientific validity, alignment with research gaps, and testability**.\n\n"
                "**Hypothesis:**\n"
                f"{hypothesis}\n\n"
                "**Identified Research Gaps:**\n"
                f"{formatted_gaps}\n\n"
                "**Instructions:**\n"
                "- Identify any **logical flaws, testability issues, or unclear assumptions**.\n"
                "- Ensure the hypothesis **clearly aligns with the research gaps**.\n"
                "- Provide **specific refinements** to improve clarity and empirical rigor.\n\n"
                "**Expected Output Format:**\n"
                "- 🔴 **Critique:** [Describe issue]\n"
                "- ✅ **Suggested Refinement:** [Provide improved version of the hypothesis]"
            )
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to generate a critique."

        return response.msgs[0].content
