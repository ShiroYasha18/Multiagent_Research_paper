import requests
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module


class HypothesisGenerationAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message=(
                "You are an expert research scientist specializing in hypothesis generation. "
                "Your task is to formulate **concise, testable, and well-justified** hypotheses "
                "that directly address research gaps identified in academic literature."

                
                "**Key Rules:**"
                
                "✔ Ensure the hypothesis is **specific, measurable, and falsifiable**."
                
                "✔ Link the hypothesis to an **identified research gap**."
                
                "✔ Clearly state the **independent and dependent variables**."
                "✔ Use **formal academic structure** (no vague claims)."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def generate_hypothesis(self, literature_review, research_gaps):
        """
        Generate a well-structured hypothesis based on research gaps.

        :param literature_review: The summarized literature review.
        :param research_gaps: A list of identified research gaps.
        :return: A concise and testable hypothesis.
        """

        if not research_gaps:
            return " No research gaps identified. Hypothesis generation canceled."

        # **Select the most critical research gap**
        primary_gap = max(research_gaps, key=len)  # Prioritizes detailed gaps

        #  Trim literature review for token efficiency
        max_review_length = 2000  # Adjust as needed
        trimmed_review = literature_review[:max_review_length] + "..." if len(literature_review) > max_review_length else literature_review

        # Formatted research gaps list
        formatted_gaps = "\n".join([f"- {gap}" for gap in research_gaps[:3]])  # Limit to top 3 gaps

        # Generate user message
        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=(
                "Based on the **literature review summary** and **identified research gaps**, "
                "formulate a **precise, testable hypothesis** addressing a key gap."
                "**Literature Review Summary:** "
                f"{trimmed_review}  "
                "**Identified Research Gaps:**"
                
                f"{formatted_gaps}"

                
                "**Instructions:**"
                
                "- Select **ONE** research gap and create a hypothesis around it."
                
                "- Ensure the hypothesis is **testable and measurable**."
                
                "- Justify why this hypothesis is relevant based on prior research."
                
                "- Specify the **independent** and **dependent variables**."

                
                "**Format Example:**"
                
                '"If [Independent Variable] is modified in [Specific Way], then [Dependent Variable] will change due to [Scientific Reasoning]."'
            )
        )

        # LLM Response Handling
        hypothesis_response = self.agent.step(user_message)
        if not hypothesis_response.msgs or not hypothesis_response.msgs[0].content.strip():
            return " AI failed to generate a hypothesis. Try again."

        hypothesis = hypothesis_response.msgs[0].content

        # Self-Reflection Loop
        reflection_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=(
                f"Critique the following hypothesis and suggest improvements:"
                "{hypothesis}"

                "Identify any logical flaws, missing variables, or vague claims. Suggest a more rigorous version of the hypothesis."
            )
        )
        reflection_response = self.agent.step(reflection_message)
        if reflection_response.msgs and reflection_response.msgs[0].content.strip():
            hypothesis += "** CritiqueReflection: **" + reflection_response.msgs[0].content


        return hypothesis