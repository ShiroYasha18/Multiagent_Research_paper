import os
import asyncio
from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import GroqConfig
from agents import (
    DataAnalysisAgent,
    ExperimentDesignAgent,
    HypothesisGenerationAgent,
    LiteratureReviewAgent,
    CriticAgent,
    ResearchWriter,
    DatasetExtractionAgent
)
from tools.pdf_generator import ReportLabPDFGenerator


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY not found. Please check your .env file.")


model = ModelFactory.create(
    model_platform=ModelPlatformType.GROQ,
    model_type=ModelType.GROQ_LLAMA_3_70B,
    api_key=groq_api_key,
    model_config_dict=GroqConfig(temperature=0.3).as_dict(),
)


hypothesis_agent = HypothesisGenerationAgent(model)
experiment_agent = ExperimentDesignAgent(model)
data_analysis_agent = DataAnalysisAgent(model)
literature_review_agent = LiteratureReviewAgent(model)
critic_agent = CriticAgent(model)
research_writer = ResearchWriter(model)
dataset_agent = DatasetExtractionAgent()
pdf_generator = ReportLabPDFGenerator()

#  Define Research Topic
topic = "Satellite Landslide detection"

#  Storage for Citations
citations = []

async def run_research():
    print("🔄 Starting Research Workflow...\n")

    #  Literature Review
    print(" Conducting Literature Review...")
    review, cited_papers, research_gaps = literature_review_agent.review_literature(topic)
    citations.extend(cited_papers)
    print(f"📚 Literature Review:\n{review}\n")

    #  Dataset Extraction from Citations
    print("🔍 Automatically Extracting Datasets from Research Papers...")
    all_datasets = []
    for paper in cited_papers:
        try:
            dataset = dataset_agent.extract_dataset(paper["link"])
            cleaned_dataset = dataset_agent.clean_dataset(dataset)
            all_datasets.append(cleaned_dataset)
            print(f" Dataset Extracted from {paper['title']}\n{cleaned_dataset.head()}\n")
        except Exception as e:
            print(f" Dataset Extraction Failed for {paper['title']}: {e}")

    #  Hypothesis Generation with Recursive Reflection
    print(" Generating Hypothesis...")
    hypothesis = hypothesis_agent.generate_hypothesis(review, research_gaps)
    print(f"📝 **Generated Hypothesis:**\n{hypothesis}\n")

    #  Hypothesis Critique with Self-Reflection
    print(" Critiquing Hypothesis...")
    critique = critic_agent.critique_hypothesis(hypothesis)
    print(f"💡 **Critique & Refinement:**\n{critique}\n")

    #  Experiment Design
    print(" Designing Experiment...")
    experiment = experiment_agent.design_experiment(hypothesis)
    print(f"🧪 **Experimental Design:**\n{experiment}\n")

    #  Data Analysis (Using Paper Comparison + XAI Integration)
    print(" Analyzing Data Across Research Papers...")
    data_analysis = data_analysis_agent.compare_findings(topic)
    print(f" **Data Analysis Insights:**\n{data_analysis}\n")

    #  Generate References Section
    reference_section = "\n".join(
        f"- {citation.get('title', 'Unknown Title')} (Source: {citation.get('link', 'No Link')})"
        for citation in citations
    )

    #  Generate Final Research Report with ReportLab
    pdf_generator.generate_pdf(
        title="Final Research Paper",
        sections={
            "Literature Review": review,
            "Identified Research Gaps": data_analysis,
            "Proposed Hypothesis": hypothesis,
            "Critique & Refinement": critique,
            "Experimental Design": experiment,
            "Key Insights & Validation": data_analysis,
            "References": reference_section,
        },
        filename="final_research_paper"
    )

    print("Final Research Paper Generated with ReportLab: final_research_paper.pdf")

# Run the research workflow
asyncio.run(run_research())
