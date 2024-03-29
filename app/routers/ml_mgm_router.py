import base64

from fastapi import APIRouter, Depends

from services.ml_manager_service import AVAILABLE_MODELS
from services.ml_manager_service import MLManagerService
from models import ModelCreationEntity
from models import ModelTrainingRequest

router = APIRouter()

@router.post("/models")
def model_creation(
        r: ModelCreationEntity, mgr = Depends(MLManagerService)
):
    if r.model not in AVAILABLE_MODELS:
        return {"status": "bad_request"}, 400

    model_uid = mgr.create_model_with_reqs(r)

    return {"id": model_uid}

@router.get("/models/{model_uid}")
def model_retrieval(model_uid: str, mgr = Depends(MLManagerService)):
    model_metadata = mgr.retrieve_model_by_id(model_uid)

    if model_metadata is None:
        return {"status": "model_not_found"}, 404

    return model_metadata

@router.post("/models/{model_uid}/train")
def model_training(
        model_uid: str, r: ModelTrainingRequest, mgr = Depends(MLManagerService)
):
    model_metadata = mgr.retrieve_model_by_id(model_uid)

    if model_metadata is None:
        print("Model not foud in DB")
        return {"status": "model_not_found"}, 404

    if model_metadata["n_features"] != len(r.feature_vector):
        print("Feature vector does not match length")
        return {"status": "bad_request"}, 400

    if model_metadata["n_classes"] <= r.label:
        print("Label does not match the number of classes")
        return {"status": "bad_request"}, 400

    new_trained = mgr.partial_train(
        model_uid, r.feature_vector, r.label
    )

    return {"id": model_uid, "n_trained": new_trained}

@router.get("/models/{model_uid}/predict")
def model_predict(
        model_uid: str, input_vector: str, mgr = Depends(MLManagerService)
):
    feature_vector = base64.b64decode(
        input_vector,
    )
    feature_vector = eval(feature_vector)

    if feature_vector is None:
        print("Feature vector empty")
        return {"status": "bad_request"}, 400

    model_metadata = mgr.retrieve_model_by_id(model_uid)

    if model_metadata is None:
        print("Model not foud in DB")
        return {"status": "model_not_found"}, 404

    if model_metadata["n_features"] != len(feature_vector):
        print("Feature vector does not match length")
        return {"status": "bad_request"}, 400

    prediction = mgr.predict(
        model_uid, feature_vector,
    )

    return {"x": feature_vector, "y": int(prediction)}

@router.get("/models")
def most_trained_models(mgr = Depends(MLManagerService)):
    return mgr.get_models_and_trained_score()
