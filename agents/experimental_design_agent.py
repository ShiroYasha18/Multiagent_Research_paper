import requests
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
from tools.memory_module import create_memory_module


class ExperimentDesignAgent:
    def __init__(self, model):
        """Initialize the ExperimentDesignAgent with a language model."""
        self.agent = ChatAgent(
            system_message=(
                "You are an expert scientific researcher specializing in experimental design. "
                "Your task is to create detailed, rigorous experimental protocols that can "
                "effectively test hypotheses. Focus on creating experiments with clear "
                "methodologies, well-defined variables, appropriate data collection methods, "
                "and robust analysis approaches."
            ),
            model=model,
            memory=create_memory_module(),
        )

    def design_experiment(self, hypothesis):
        """Designs an experiment based on the hypothesis."""
        prompt = f"""
        Design a detailed experiment to test the following hypothesis:
        
        {hypothesis}
        
        Please include:
        1. Methodology (detailed experimental setup)
        2. Variables (independent, dependent, and control variables)
        3. Data collection methods (instruments, measurements, frequency)
        4. Analysis approach (statistical methods, data processing)
        5. Expected outcomes (what results would support or refute the hypothesis)
        6. Potential limitations and how to address them
        
        Format your response as a structured experimental protocol that could be implemented by researchers.
        """
        
        message = BaseMessage(
            role_name="User",
            role_type=RoleType.USER,
            meta_dict={},
            content=prompt
        )
        
        try:
            response = self.agent.step(message)
            if response and response.msgs and len(response.msgs) > 0:
                return response.msgs[0].content
            else:
                return "Error: No response generated for experiment design."
        except Exception as e:
            return f"Error in experiment design generation: {str(e)}"
