from pydantic import BaseModel

class ModelCreationEntity(BaseModel):
    model: str
    params: dict
    num_features: int
    num_classes: int
