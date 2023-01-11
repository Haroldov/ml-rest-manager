import mysql.connector
import os
import pickle
import uuid

class MySQLRepository():

    def __init__(self):
        self.config = {
            "user": os.getenv("MYSQL_USER", ""),
            "password": os.getenv("MYSQL_ROOT_PASSWORD", "PASSWORD"),
            "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
            "port": 3306,
            "database": os.getenv("MYSQL_DATABASE", "public"),
            "raise_on_warnings": True,
        }
        self.pool_name = "MYSQL_DB_POOL"
        self.pool_size = 15
        self.queries_path = "./db/queries/"

        try:
            cnx = mysql.connector.connect(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                **self.config
            )
        except Exception as e:
            print("Exception connecting to db:", e)


    def _connect(self):
        try:
            cnx = mysql.connector.connect(
                pool_name=self.pool_name,
            )

            cursor = cnx.cursor()

            return (cnx, cursor)
        except Exception as e:
            print("Exception connecting to db:", e)

            return None

    def create_tables_on_startup(self):
        with open(self.queries_path + "create_tables.sql", "r") as f:
            queries = f.read()

        cnx, cursor = self._connect()
        for query in queries.split(";")[:-1]:
            try:
                cursor.execute(query)
            except Exception as e:
                print("Exception executing query", e)

        cursor.close()
        cnx.close()

    def insert_or_update_model(
            self,
            model_uid,
            serialized_model,
            model_type = "",
            init_params = "{}",
            num_classes = 0,
            num_features = 0,
    ):
        cnx, cursor = self._connect()

        with open(self.queries_path + "insert_binary_model.sql", "r") as f:
           insert_binary_query = f.read()
        
        cursor.execute(
            insert_binary_query,
            [str(model_uid), serialized_model],
        )

        with open(self.queries_path + "insert_model_metadata.sql", "r") as f:
           insert_metadata_query = f.read()

        cursor.execute(
            insert_metadata_query,
	    [str(model_uid), model_type, init_params, num_classes, num_features, 0],
        )
        
        cnx.commit()

        cursor.close()
        cnx.close()

    def retrieve_model(self, model_uid):
        cnx, cursor = self._connect()

        with open(self.queries_path + "retrieve_model_metadata_by_id.sql", "r") as f:
            retrieve_metadata_query = f.read()

        cursor.execute(
            retrieve_metadata_query,
            [model_uid],
        )

        data = cursor.fetchone()

        cursor.close()
        cnx.close()

        if data is None:
            return None

        
        return {
            "model_binary": data[0],
            "model_type": data[1],
            "init_params": data[2],
            "num_classes": data[3],
            "num_features": data[4],
            "num_training": data[5],
        }

    def retrieve_models_by_trained_score(self):
        cnx, cursor = self._connect()

        with open(self.queries_path + "trained_score.sql", "r") as f:
            retrieve_metadata_query = f.read()

        cursor.execute(
            retrieve_metadata_query,
        )

        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        return [{
            "model_id": item[0],
            "model_type": item[1],
            "num_training": item[2],
            "trained_score": item[3],
        } for item in data]
