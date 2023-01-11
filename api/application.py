from flask import Flask , request
from models.model_creation_entity import model_creation_request
from models.model_training_entity import model_training_request
from dotenv import load_dotenv

from db.mysql_repository import MySQLRepository
from services.ml_manager_service import MLManagerService

load_dotenv()

application = Flask(__name__)

db = MySQLRepository()
db.create_tables_on_startup()

mgr = MLManagerService(db)

@application.route("/health", methods=["GET"])
def health_check():
    return {"message": "Ok"}


@application.route("/models", methods=["POST"])
def model_creation():
    r = request.get_json()

    try:
        r_entity = model_creation_request(**r)
    except TypeError as e:
        print("Bad Request: ", r)
        print("Message: ", e)

        return {"status": "bad_request"}, 400

    model_uid = mgr.create_model_with_reqs(r_entity)

    return {"id": model_uid}

@application.route("/models/<model_uid>", methods=["GET"])
def model_retrieval(model_uid):
    model_metadata = mgr.retrieve_model_by_id(model_uid)

    if model_metadata is None:
        return {"status": "model_not_found"}, 404

    return model_metadata

@application.route("/models/<model_uid>/train", methods=["POST"])
def model_training(model_uid):
    r = request.get_json()

    try:
        r_entity = model_training_request(**r)
    except TypeError as e:
        print("Bad Request: ", r)
        print("Message: ", e)

        return {"status": "bad_request"}, 400

    model_metadata = mgr.retrieve_model_by_id(model_uid)

    if model_metadata is None:
        print("Model not foud in DB")
        return {"status": "model_not_found"}, 404

    if model_metadata["d"] != len(r_entity.feature_vector):
        print("Feature vector does not match length")
        return {"status": "bad_request"}, 400

    if model_metadata["n_classes"] < r_entity.label:
        print("Label does not match the number of classes")
        return {"status": "bad_request"}, 400

    new_trained = mgr.partial_train(
        model_uid, r_entity.feature_vector, r_entity.label
    )

    return {"id": model_uid, "n_trained": new_trained}
