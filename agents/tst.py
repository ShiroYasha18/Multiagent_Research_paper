from agents.literature_review_agent import LiteratureReviewAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import GroqConfig
import os
from dotenv import load_dotenv

# ✅ Load API Keys
load_dotenv()

# ✅ Initialize Model
model = ModelFactory.create(
    model_platform=ModelPlatformType.GROQ,
    model_type=ModelType.GROQ_LLAMA_3_70B,
    api_key=os.getenv("GROQ_API_KEY"),
    model_config_dict=GroqConfig(temperature=0.3).as_dict(),
)

# ✅ Initialize Literature Review Agent
literature_agent = LiteratureReviewAgent(model)

# ✅ Run Literature Review
topic = " Handwritten Answers evaluation using Multimodal AI"
print(f"\n🔍 Running Literature Review Test on: **{topic}**\n")
summary, papers, gaps = literature_agent.review_literature(topic)

# ✅ Print Results
print("\n📚 **Generated Literature Review Summary:**")
print(summary)
