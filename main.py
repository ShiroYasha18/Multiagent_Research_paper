# main.py

from agents.hypothesis_generation_agent import create_hypothesis_generation_agent
from agents.experimental_design_agent import create_experimental_design_agent
from agents.data_analysis_agent import create_data_analysis_agent
from agents.literature_review_agent import create_literature_review_agent
from camel.societies import Society

def main():
    # Initialize agents
    hypothesis_agent = create_hypothesis_generation_agent()
    experimental_design_agent = create_experimental_design_agent()
    data_analysis_agent = create_data_analysis_agent()
    literature_review_agent = create_literature_review_agent()

    # Create a society of agents
    society = Society([
        hypothesis_agent,
        experimental_design_agent,
        data_analysis_agent,
        literature_review_agent
    ])

    # Define a research task
    research_task = "Investigate the potential of CRISPR-Cas9 in treating genetic disorders."

    # Assign the task to the society
    society.assign_task(research_task)

    # Run the society to perform the task
    society.run()

if __name__ == "__main__":
    main()
