from pydantic import BaseModel

class ModelTrainingRequest(BaseModel):
    feature_vector: list
    label: int
