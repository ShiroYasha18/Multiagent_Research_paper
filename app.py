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
)
from tools.pdf_generator import generate_pdf

# ✅ Load API Key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY not found. Please check your .env file.")

# ✅ Initialize Model with Groq LLaMA 3
model = ModelFactory.create(
    model_platform=ModelPlatformType.GROQ,
    model_type=ModelType.GROQ_LLAMA_3_70B,
    api_key=groq_api_key,
    model_config_dict=GroqConfig(temperature=0.3).as_dict(),
)

# ✅ Initialize AI Research Agents
hypothesis_agent = HypothesisGenerationAgent(model)
experiment_agent = ExperimentDesignAgent(model)
data_analysis_agent = DataAnalysisAgent(model)
literature_review_agent = LiteratureReviewAgent(model)
critic_agent = CriticAgent(model)
research_writer = ResearchWriter(model)

# ✅ Define Research Topic
topic = "Deep Learning in Breast Cancer detection"

# ✅ Storage for Citations
citations = []


async def run_research():
    print("🔄 Starting Research Workflow...\n")

    # 🔹 Literature Review
    print("🔹 Conducting Literature Review...")
    review, cited_papers, research_gaps = literature_review_agent.review_literature(topic)

    citations.extend(cited_papers)
    print(f"📚 Literature Review:\n{review}\n")

    print("🔹 Generating Hypothesis...")
    hypothesis = hypothesis_agent.generate_hypothesis(review, research_gaps)
    print(f"📝 **Generated Hypothesis:**\n{hypothesis}\n")




    # 🔹 Experiment Design
    print("🔹 Designing Experiment...")
    experiment = experiment_agent.design_experiment(hypothesis)
    print(f"🧪 **Experimental Design:**\n{experiment}\n")

    # 🔹 Data Analysis (Using Paper Comparison)
    print("🔹 Analyzing Data Across Research Papers...")
    data_analysis = data_analysis_agent.compare_research_findings(topic)
    print(f"📊 **Data Analysis Insights:**\n{data_analysis}\n")

    # ✅ Generate Final Research Report
    research_summary = f"""
🔹 **Literature Review:**  
{review}  

🔹 **Identified Research Gaps:**  
{data_analysis}  

🔹 **Proposed Hypothesis:**  
{hypothesis}  

 

🔹 **Experimental Design:**  
{experiment}  

🔹 **Key Insights & Validation:**  
{data_analysis}  
"""

    # ✅ Generate References Section
    reference_section = "\n📌 **References:**\n" + "\n".join(
        f"- {citation.get('title', 'Unknown Title')} (Source: {citation.get('link', 'No Link')})"
        for citation in citations
    )

    # ✅ Save Final Research Paper as PDF
    generate_pdf(
        {"Final Research Paper": research_summary, "References": reference_section},
        "final_research_paper.pdf",
    )
    print("📄 Final Research Paper Generated: final_research_paper.pdf")


# Run the research workflow
asyncio.run(run_research())
