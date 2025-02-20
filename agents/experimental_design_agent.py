import requests
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module
from datetime import datetime


class ExperimentDesignAgent:
    def __init__(self, model):
        self.agent = ChatAgent(
            system_message="You are an expert in scientific experiment design. Your task is to propose rigorous experiments that validate hypotheses.",
            model=model,
            memory=create_memory_module(),
        )

    def design_experiment(self, hypothesis):
        """Generate an experiment that rigorously tests the hypothesis."""
        user_message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=f"Design an experiment to rigorously test the following hypothesis. Include methodology, variables, and evaluation metrics:\n\n{hypothesis}"
        )

        response = self.agent.step(user_message)
        if not response.msgs:
            return "❌ AI failed to generate an experiment. Try again."

        return response.msgs[0].content
