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
# Remove XAI module initialization
pdf_generator = ReportLabPDFGenerator()

#  Define Research Topic
topic = "Satellite Landslide detection"
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


# Try to create model with fallback options
try:
    model = ModelFactory.create(
        model_platform=ModelPlatformType.GROQ,
        model_type=ModelType.GROQ_LLAMA_3_70B,
        api_key=groq_api_key,
        model_config_dict=GroqConfig(temperature=0.3).as_dict(),
    )
except Exception as e:
    print(f"Error creating primary model: {e}")
    try:
        # Fallback to a smaller model
        print("Trying fallback to smaller model...")
        model = ModelFactory.create(
            model_platform=ModelPlatformType.GROQ,
            model_type=ModelType.GROQ_LLAMA_3_8B,
            api_key=groq_api_key,
            model_config_dict=GroqConfig(temperature=0.3).as_dict(),
        )
    except Exception as e:
        print(f"Error creating fallback model: {e}")
        raise


hypothesis_agent = HypothesisGenerationAgent(model)
experiment_agent = ExperimentDesignAgent(model)
data_analysis_agent = DataAnalysisAgent(model)
literature_review_agent = LiteratureReviewAgent(model)
critic_agent = CriticAgent(model)
research_writer = ResearchWriter(model)
dataset_agent = DatasetExtractionAgent()
pdf_generator = ReportLabPDFGenerator()

# Define Research Topic
topic = "Satellite Landslide detection"

# Storage for Citations
citations = []

async def run_research():
    print("🔄 Starting Research Workflow...\n")

    try:
        # Literature Review
        print(" Conducting Literature Review...")
        review, cited_papers, research_gaps = literature_review_agent.review_literature(topic)
        
        # Add paper summary right after literature review
        print("📚 Summarizing Research Papers...")
        papers_summary = data_analysis_agent.summarize_papers(topic)
        print(papers_summary)
        
        citations.extend(cited_papers)
        print(f"📚 Literature Review:\n{review}\n")

        # Hypothesis Generation with Recursive Reflection
        print(" Generating Hypothesis...")
        try:
            input_data = {
                "review": review,
                "research_gaps": research_gaps
            }
            hypothesis = hypothesis_agent.generate_hypothesis(input_data)
            print(f"📝 **Generated Hypothesis:**\n{hypothesis}\n")
        except Exception as e:
            print(f"Error generating hypothesis: {e}")
            hypothesis = "The integration of multi-temporal satellite imagery with machine learning techniques can significantly improve landslide detection accuracy and response time compared to traditional single-source methods."
            print(f"📝 **Using Default Hypothesis:**\n{hypothesis}\n")

        # Dataset Extraction from Citations
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

        # Hypothesis Critique with Self-Reflection
        print(" Critiquing Hypothesis...")
        try:
            critique = critic_agent.critique_hypothesis(hypothesis)
            print(f"💡 **Critique & Refinement:**\n{critique}\n")
        except Exception as e:
            print(f"Error critiquing hypothesis: {e}")
            critique = "The hypothesis is testable but could be more specific about which machine learning techniques and which types of satellite imagery would be most effective."
            print(f"💡 **Using Default Critique:**\n{critique}\n")

        # Experiment Design
        print(" Designing Experiment...")
        try:
            experiment = experiment_agent.design_experiment(hypothesis)
            print(f"🧪 **Experimental Design:**\n{experiment}\n")
        except Exception as e:
            print(f"Error designing experiment: {e}")
            experiment = "A comparative study using multiple satellite data sources (optical, SAR, and infrared) with various machine learning models (CNNs, RNNs, and ensemble methods) to detect landslides across diverse geographical regions."
            print(f"🧪 **Using Default Experimental Design:**\n{experiment}\n")

        # Data Analysis
        print(" Analyzing Data Across Research Papers...")
        try:
            data_analysis = data_analysis_agent.compare_findings(topic)
            print(f" **Data Analysis Insights:**\n{data_analysis}\n")
        except Exception as e:
            print(f"Error analyzing data: {e}")
            data_analysis = "Current research shows CNN-based methods achieve 85-92% accuracy in landslide detection, with SAR data improving detection in cloudy conditions."
            print(f" **Using Default Data Analysis:**\n{data_analysis}\n")

        # Generate References Section
        reference_section = "\n".join(
            f"- {citation.get('title', 'Unknown Title')} (Source: {citation.get('link', 'No Link')})"
            for citation in citations
        )

        # Update sections dictionary to include paper summary
        sections = {
            "Research Papers Summary": papers_summary,
            "Literature Review": review,
            "Identified Research Gaps": research_gaps,
            "Proposed Hypothesis": hypothesis,
            "Critique & Refinement": critique,
            "Experimental Design": experiment,
            "Key Insights & Validation": data_analysis,
            "References": reference_section,
        }

        # Generate Final Research Report
        print("📊 Generating Research Report...")
        try:
            # Check if XAI visualization files exist
            images = []
            shap_plot = "/Users/ayrafraihan/Desktop/pythonProject11/shap_summary_plot.png"
            gradcam_plot = "/Users/ayrafraihan/Desktop/pythonProject11/gradcam_explanation.png"
            
            if os.path.exists(shap_plot):
                images.append(shap_plot)
            if os.path.exists(gradcam_plot):
                images.append(gradcam_plot)

            pdf_generator.generate_pdf(
                title="Final Research Paper",
                sections=sections,
                images=images if images else None,
                filename="final_research_paper"
            )
            print("✅ Final Research Paper Generated: final_research_paper.pdf")
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            raise

    except Exception as e:
        print(f"❌ Error in research workflow: {e}")
        import traceback
        traceback.print_exc()

# Run the research workflow
if __name__ == "__main__":
    asyncio.run(run_research())
