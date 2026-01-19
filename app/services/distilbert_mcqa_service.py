from config import settings
from os import path

import numpy as np
import pickle
import uuid
import json
import torch

from services.lifespan_model_load import models



class DistilBertMCQAService:

    def __init__(self):
        self.model = models[settings.distilbert_model_name][0]
        self.tokenizer = models[settings.distilbert_model_name][1]

    def predict(
        self, question: str, choices_map: dict
    ):
        qa_pairs = [[question, choice] for choice in choices_map.values()]
        encoding: BatchEncoding = self.tokenizer(qa_pairs, return_tensors='pt', padding=True)
        inputs = {k: v.unsqueeze(0) for k, v in encoding.items()}

        with torch.inference_mode():
            model_output: MultipleChoiceModelOutput = self.model(**inputs)
            max_index = torch.argmax(model_output.logits)

        choices = tuple(choices_map.values())
        predicted_choice = choices[max_index]

        return predicted_choice
