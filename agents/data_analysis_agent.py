import numpy as np
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module


class DataAnalysisAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message="You are an AI data analyst specializing in research comparison. Your task is to identify numerical discrepancies and validate research gaps across multiple papers.",
            model=model,
            memory=create_memory_module(),
        )

    def extract_numerical_findings(self, research_papers):
        """
        Extracts numerical values from research papers for statistical comparison.
        Returns a dictionary mapping paper titles to extracted numbers.
        """
        numerical_findings = {}

        for paper in research_papers:
            lines = paper.split(". ")
            title = lines[0] if len(lines) > 1 else "Untitled Paper"
            numbers = [float(num) for num in paper.split() if num.replace('.', '', 1).isdigit()]

            if numbers:
                numerical_findings[title] = numbers

        return numerical_findings

    def compare_research_findings(self, research_papers):
        """
        Compares research findings across multiple papers and identifies inconsistencies.
        """
        if len(research_papers) < 2:
            return "❌ Not enough data for comparison. Provide at least two research papers."

        numerical_findings = self.extract_numerical_findings(research_papers)

        if not numerical_findings:
            return "❌ No numerical data extracted from research papers."

        # Compute mean and variance for comparison
        summary = "📊 **Research Paper Comparison:**\n"
        values_list = []

        for title, values in numerical_findings.items():
            mean_val = np.mean(values)
            variance_val = np.var(values)
            values_list.extend(values)

            summary += f"- **{title}**: Mean = {mean_val:.2f}, Variance = {variance_val:.2f}\n"

        # Identify inconsistencies
        overall_variance = np.var(values_list)
        max_val, min_val = max(values_list), min(values_list)
        difference = max_val - min_val

        if difference > 10:  # Threshold for inconsistency detection
            summary += f"\n❗ **Potential Research Gap Identified:** Significant variance in reported results. Numerical findings range from {min_val} to {max_val}, suggesting inconsistent methodologies or data biases.\n"

        return summary

    def validate_research_gaps(self, research_papers):
        """
        Uses an AI model to analyze and validate research gaps from identified inconsistencies.
        """
        comparison_results = self.compare_research_findings(research_papers)

        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=f"Based on the following comparative research analysis, validate the identified research gaps and suggest ways to bridge them:\n\n{comparison_results}"
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to validate research gaps."

        return response.msgs[0].content
