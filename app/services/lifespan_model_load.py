from config import settings
from os import path
from contextlib import asynccontextmanager
from fastapi import FastAPI

from transformers import DistilBertForMultipleChoice, DistilBertTokenizerFast

models: dict[str, object] = {}

# This is to load models at the startup of the FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    models[settings.distilbert_model_name] = load_distilbert_model()

    yield

    ml_models.clear()

def load_distilbert_model() -> (DistilBertForMultipleChoice, DistilBertTokenizerFast):
    model_path: str = path.join(
        settings.models_base_path,
        settings.distilbert_model_name,
        settings.distilbert_model_version,    
    )

    tokenizer: DistilBertTokenizerFast = DistilBertTokenizerFast.from_pretrained(model_path)
    model: DistilBertForMultipleChoice = DistilBertForMultipleChoice.from_pretrained(model_path)
    model.eval()

    return model, tokenizer