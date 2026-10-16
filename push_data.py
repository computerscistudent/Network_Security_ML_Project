import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# if MONGODB_URL:
#     MONGODB_URL_L = MONGODB_URL.split(".")
#     MONGODB_URL = MONGODB_URL_L[:-1]
# print(".".join(MONGODB_URL)) #type:ignore

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from network_security.logging import logger
from network_security.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self,file_path,database,collection):
        self.file_path = file_path
        self.database = database
        self.collection = collection

        try:
            self.records = self.cv_to_json_converter()
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def cv_to_json_converter(self):
        try:
            data = pd.read_csv(self.file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_data_mongodb(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            self.database = self.mongo_client[self.database] #type:ignore

            self.collection = self.database[self.collection] #type:ignore
            self.collection.insert_many(self.records)

            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "ABHIMANYU_DS"
    collection = "Network_Data"
    networkobj = NetworkDataExtract(FILE_PATH,DATABASE,collection)
    no_of_records = networkobj.insert_data_mongodb()
    print(no_of_records)