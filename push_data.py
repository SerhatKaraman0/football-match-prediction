import os 
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

ca = certifi.where()


class DataExtract:
    def __init__(self) -> None:
        try:
            pass
        except Exception as e:
            raise ETLPipelineException(e, sys)
        
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            return records
        
        except Exception as e:
            raise ETLPipelineException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.records = records
            self.collection = collection

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)
        
        except Exception as e:
            raise ETLPipelineException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "data/phisingData.csv"
    DATABASE = "ETL_PIPELINE"
    COLLECTION = "NETWORK_SECURITY_DATA"

    obj = DataExtract()
    records = obj.csv_to_json_converter(FILE_PATH)
    number_of_records = obj.insert_data_mongodb(records, DATABASE, COLLECTION)

    print(number_of_records)




