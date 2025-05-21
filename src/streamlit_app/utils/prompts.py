from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

classification_prompt = ChatPromptTemplate.from_template(
    """
You are my personal representative. Recruiters might ask you about my skillset and project portfolio and other related things.
Pick the most relevant category for the user input.

Current user input:
{input}
"""
)

class ClassificationTag(BaseModel):
    category: str = Field(
        description="Decide for which category user input is related the most.",
        enum=["about Me", "experience", "programming", "projects", "development", "other"]
    )