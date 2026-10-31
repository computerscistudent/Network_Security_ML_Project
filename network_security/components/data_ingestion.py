from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
import sys
import numpy as np
import os
from typing import List
import pymongo
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_collection_as_dataframe(self):
        """
        Export collection data as dataframe
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[database_name] #type:ignore
            collection = self.database[collection_name] #type:ignore

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df = df.drop("_id",axis=1)

            df.replace(to_replace="na", value=np.nan,inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_data_into_feature_store(self,df:pd.DataFrame):
        """
        Export data into feature store
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            df.to_csv(feature_store_file_path,index=False,header=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self,df:pd.DataFrame):
        """
        Split data into train and test
        """
        try:
            train_set,test_set = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the data")

            logging.info(f"Exporting train and test data into {self.data_ingestion_config.data_ingestion_dir} directory")
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path

            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_set.to_csv(train_file_path,index=False,header=True)
            test_set.to_csv(test_file_path,index=False,header=True)

            logging.info(f"Exported train and test data into {self.data_ingestion_config.data_ingestion_dir} directory")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        """
        Initiates the data ingestion
        """
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            dataingestion_artifact = DataIngestionArtifact(
                data_ingestion_dir=self.data_ingestion_config.data_ingestion_dir,
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return dataingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)