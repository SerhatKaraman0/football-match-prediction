import os 
import sys
import numpy as np
import pandas as pd

##################################################################################
## Common Constant Variables 
##################################################################################

SCHEMA_FILE_PATH      = os.path.join("data_schema", "schema.yaml")
TARGET_COLUMN         = "Result"
PIPELINE_NAME :  str  = "training_pipeline"
ARTIFACT_DIR  :  str  = "artifacts"
FILE_NAME     :  str  = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME  = "test.csv"

##################################################################################
## Data Ingestion Constant Variables 
##################################################################################

DATA_INGESTION_COLLECTION_NAME              : str   = "NETWORK_SECURITY_DATA"
DATA_INGESTION_DATABASE_NAME                : str   = "ETL_PIPELINE"
DATA_INGESTION_DIR_NAME                     : str   = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR            : str   = "feature_store"
DATA_INGESTION_INGESTED_DIR                 : str   = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO       : float = 0.2

##################################################################################
## Data Validation Constant Variables 
##################################################################################

DATA_VALIDATION_DIR_NAME               : str    = "data_validation"
DATA_VALIDATION_VALID_DIR              : str    = "validated"
DATA_VALIDATION_INVALID_DIR            : str    = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR       : str    = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str    = "report.yaml"


##################################################################################
## Data Transformation Constant Variables 
##################################################################################
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
DATA_TRANSFORMATION_DIR_NAME                : str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR    : str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR  : str = "transformed_object"
DATA_TRANSFORMATION_IMPUTER_PARAMS          : dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}

##################################################################################
## Model Trainer Constant Variables 
##################################################################################
MODEL_FILE_NAME                                     : str = "model.pkl"
MODEL_TRAINER_DIR_NAME                              : str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR                     : str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME                    : str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE                        : float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD  : float = 0.05
SAVED_MODEL_DIR = os.path.join("saved_models")

TRAINING_BUCKET_NAME = "etlprojectpipeline"