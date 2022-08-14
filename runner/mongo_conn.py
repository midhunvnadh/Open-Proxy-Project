import os
from pymongo import MongoClient
from time import sleep


def mongo_client():
    CONNECTION_STRING = os.getenv("MONGO_CONN_URL")
    try:
        if CONNECTION_STRING is None:
            raise Exception("Please set MONGO_CONN_URL environment variable")
        client = MongoClient(CONNECTION_STRING)
        return client
    except Exception as e:
        print(e)
        sleep(5)
        exit(1)
