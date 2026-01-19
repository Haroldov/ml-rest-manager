from fastapi import Depends
from config import settings
from os import path


import numpy as np
import pickle
import uuid
import json

from services.distilbert_mcqa_service import DistilBertMCQAService

class MCQAManagerService:

    MODEL_REGISTRY: dict[str, object] = {} 

    def __init__(self, distilbertmcqa = Depends(DistilBertMCQAService)):
        self.MODEL_REGISTRY[settings.distilbert_model_name] = distilbertmcqa

    def predict(
        self, name: str, question: str, choices_map: dict
    ):
        model_service = self.MODEL_REGISTRY.get(name)
        if not model_service:   
            raise ValueError(f"Model {name} not found in registry.")

        return model_service.predict(question, choices_map)