import base64

from fastapi import APIRouter, Depends
from config import settings

from services.mcqa_manager_service import MCQAManagerService
from entities.mcqa_entities import MCQARequest, MCQAResponse

router = APIRouter()

@router.post("/models/mcqa/{model_name}/predict")
def model_predict(
        model_name: str, r: MCQARequest, mcqa = Depends(MCQAManagerService)
):
    if len(model_name) == 0:
        return {"status": "bad_request", "error": "Model_not_recognized"}, 400

    try:
        prediction: str = mcqa.predict(
            name=model_name,
            question=r.question,
        choices_map=r.choices_map
        )
    except ValueError as ve:
        return {"status": "bad_request", "error": str(ve)}, 400

    return MCQAResponse(model_name=model_name, prediction=prediction)
