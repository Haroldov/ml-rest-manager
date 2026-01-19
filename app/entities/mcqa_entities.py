from pydantic import BaseModel
from config import settings

class MCQARequest(BaseModel):
    question: str
    choices_map: dict[str, str]

class MCQAResponse(BaseModel):
    model_name: str = settings.distilbert_model_name
    prediction: str
