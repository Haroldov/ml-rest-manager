import numpy as np
import pickle
import uuid
import json

from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.linear_model import SGDClassifier

from db.mysql_repository import MySQLRepository

AVAILABLE_MODELS = {
    "MLPClassifier": MLPClassifier,
    "CategoricalNB": CategoricalNB,
    "SGDClassifier": SGDClassifier,
}

class MLManagerService():

    def __init__(self, db):
        self.db = db

    def create_model_with_reqs(self, r_entity):
        clf = AVAILABLE_MODELS[
            r_entity.model
        ](**r_entity.params)

        serialized_model = pickle.dumps(clf)
        model_uid = uuid.uuid4()

        self.db.insert_or_update_model(
            model_uid,
            serialized_model,
            r_entity.model,
            json.dumps(r_entity.params),
            r_entity.num_classes,
            r_entity.num_features,
        )

        return model_uid

    def retrieve_model_by_id(self, model_uid):
        data = self.db.retrieve_model(model_uid)

        if data is None:
            return None


        return {
            "model": data["model_type"],
            "params": json.loads(data["init_params"]),
            "d": data["num_features"],
            "n_classes": data["num_classes"],
            "n_trained": data["num_training"],
        }

    def partial_train(
            self, model_uid, features_sample, label
    ):
        data = self.db.retrieve_model(model_uid)

        if data is None:
            return None

        clf = pickle.loads(data["model_binary"])

        np_feature_vector = np.asarray(features_sample).reshape(
            (-1, data["num_features"])
        )
        np_label_vector = np.asarray(label).ravel()
        classes = np.asarray(range(data["num_classes"]))

        clf.partial_fit(
            X=np_feature_vector,
            y=np_label_vector,
            classes=classes
        )

        serialized_model = pickle.dumps(clf)

        self.db.insert_or_update_model(
            model_uid,
	    serialized_model,
        )

        return self.retrieve_model_by_id(model_uid)["n_trained"]

    def predict(
            self, model_uid, feature_sample
    ):
        data = self.db.retrieve_model(model_uid)

        if data is None:
            return None

        clf = pickle.loads(data["model_binary"])

        np_feature_vector = np.asarray(feature_sample).reshape(
            (-1, data["num_features"])
        )

        label = clf.predict(
            X=np_feature_vector,
        )[0]

        return label

    def get_models_and_trained_score(self):
        data = self.db.retrieve_models_by_trained_score()

        return {
           "models": [
               {
                   "id": item["model_id"],
                   "model": item["model_type"],
                   "n_trained": item["num_training"],
                   "training_score": float(item["trained_score"])
               } for item in data
           ]
       }
