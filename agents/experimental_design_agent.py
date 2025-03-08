import requests
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module


class ExperimentDesignAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message=(
                "You are a top-tier scientific research expert specializing in designing practical and "
                "well-structured experiments to rigorously validate hypotheses. "
                "Your goal is to create an experiment that meets **real-world feasibility criteria** "
                "while maintaining strong scientific rigor.\n\n"
                "**Ensure the experiment includes:**\n"
                "1️⃣ **Clear Methodology:** Step-by-step plan for conducting the experiment.\n"
                "2️⃣ **Variables & Controls:** Define independent, dependent, and control variables.\n"
                "3️⃣ **Data Collection & Metrics:** Specify evaluation methods and statistical validation.\n"
                "4️⃣ **Feasibility & Justification:** Explain why this experiment is practical & achievable.\n"
                "5️⃣ **Failure Scenarios & Adjustments:** Identify potential pitfalls and adaptations."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def design_experiment(self, hypothesis):
        """Generate a structured, **real-world applicable** experiment for the hypothesis."""
        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=(
                f"📌 **Hypothesis to Validate:**\n{hypothesis}\n\n"
                "**🔬 Design an experiment that adheres to the following structure:**\n"
                "1️⃣ **Step-by-Step Methodology:** Describe the exact steps required to conduct the experiment.\n"
                "2️⃣ **Key Variables & Controls:** Define independent, dependent, and control variables.\n"
                "3️⃣ **Data Collection & Validation:** Specify metrics, statistical techniques, and expected results.\n"
                "4️⃣ **Real-World Feasibility:** Justify how this experiment can be executed with available resources.\n"
                "5️⃣ **Failure Handling:** Outline potential obstacles and how they can be mitigated.\n\n"
                "**STRICT RULE:** The experiment must be **highly relevant** to the given hypothesis and follow "
                "a rigorous yet **practical** scientific methodology."
            )
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to generate an experiment. Try again."

        return response.msgs[0].content
