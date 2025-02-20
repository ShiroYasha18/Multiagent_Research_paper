import os
from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import  Gemini_API_PARAMS, GeminiConfig
from agents import (
    DataAnalysisAgent,
    ExperimentDesignAgent,
    HypothesisGenerationAgent,
    LiteratureReviewAgent,
    CriticAgent,
    ResearchWriter,
)
from tools.pdf_generator import generate_pdf

load_dotenv()
google = os.getenv("GOOGLE_API_KEY")
if not google:
    raise EnvironmentError("GOOGLE_API_KEY not found. Please check your .env file.")

model = ModelFactory.create(
    model_platform=ModelPlatformType.GEMINI,
    model_type=ModelType.GEMINI_1_5_FLASH ,
    api_key=google,
    model_config_dict=GeminiConfig(temperature=0.7).as_dict(),
)

hypothesis_agent = HypothesisGenerationAgent(model)
experiment_agent = ExperimentDesignAgent(model)
data_analysis_agent = DataAnalysisAgent(model)
literature_review_agent = LiteratureReviewAgent(model)
critic_agent = CriticAgent(model)
research_writer = ResearchWriter(model)

topic = "AI-powered test automation tools in software testing"

citations = []

max_iterations = 5
for iteration in range(1, max_iterations + 1):
    print(f"🔄 Iteration {iteration}...")

    print("🔹 Conducting Literature Review...")
    review, cited_papers = literature_review_agent.review_literature(topic)
    citations.extend(cited_papers)
    print(f"📚 Literature Review:\n{review}\n")

    print("🔹 Generating Hypothesis...")
    hypothesis = hypothesis_agent.generate_hypothesis(review)
    print(f"📝 Hypothesis:\n{hypothesis}\n")

    print("🔹 Critiquing Hypothesis...")
    critique = critic_agent.critique_hypothesis(hypothesis)
    print(f"🧐 Critique:\n{critique}\n")

    print("🔹 Refining Hypothesis...")
    improved_hypothesis = hypothesis_agent.generate_hypothesis(critique)
    print(f"🔄 Improved Hypothesis:\n{improved_hypothesis}\n")

    print("🔹 Designing Experiment...")
    experiment = experiment_agent.design_experiment(improved_hypothesis)
    print(f"🧪 Experimental Design:\n{experiment}\n")

    print("🔹 Analyzing Data Across Research Papers...")
    data_analysis = data_analysis_agent.compare_research_findings(topic)
    print(f"📊 Data Analysis Insights:\n{data_analysis}\n")

    if "validated" in data_analysis.lower():
        print("✅ Research Workflow Completed Successfully!")
        break

else:
    print("⚠️ Maximum iterations reached. Consider refining the topic.")

research_summary = f"""
🔹 **Literature Review:**  
{review}  

🔹 **Hypothesis:**  
{hypothesis}  

🔹 **Critique & Refinement:**  
{critique}  
{improved_hypothesis}  

🔹 **Experiment Design:**  
{experiment}  

🔹 **Data Analysis & Research Gaps:**  
{data_analysis}  

🔹 **Limitations & Future Work:**  
1. **Limited Generalization:** Results are based on AI test automation tools and may not generalize to all applications.  
2. **Dataset Bias:** The experiment relies on public datasets, which may introduce biases affecting performance evaluations.  
3. **Real-World Deployment:** While AI-based automation shows promising results, production environments need further validation.  
4. **Future Research Directions:** Scaling AI-based automation to large, enterprise-grade software remains an open challenge.  
"""

reference_section = "\n📌 **References:**\n" + "\n".join(f"- {citation}" for citation in set(citations))

generate_pdf(
    {"Final Research Paper": research_summary, "References": reference_section},
    "final_research_paper.pdf",
)
print("📄 Final Research Paper Generated: final_research_paper.pdf")
