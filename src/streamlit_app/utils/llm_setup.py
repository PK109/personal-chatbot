from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from .prompts import ClassificationTag

load_dotenv()
llm_validate = init_chat_model("gemini-2.0-flash-lite", model_provider="google_genai")
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
structured_llm = llm_validate.with_structured_output(ClassificationTag)
