from network_security.components.data_ingestion import DataIngestion
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig
import sys


if __name__=="__main__":
    try:
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiating data ingestion")
        dataingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(dataingestion_artifact)
        logging.info("Data ingestion completed successfully")
    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(e,sys)