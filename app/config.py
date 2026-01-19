from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ML API"
    models_base_path: str = "./models/"

    distilbert_model_name: str = "distilbert_mcqa"
    distilbert_model_version: str = "v0.0.1"


settings = Settings()
