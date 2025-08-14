import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from etl_project.constants.training_pipeline import TARGET_COLUMN
from etl_project.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from etl_project.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from etl_project.entity.config_entity import DataTransformationConfig
from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                       data_transformation_config: DataTransformationConfig) -> None:
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise ETLPipelineException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ETLPipelineException(e, sys)
    
    def get_data_transformer_object(cls) -> Pipeline:
        logging.info("Entered get_data_transformer_object of Data Transformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialize KNN Imputer with params {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise ETLPipelineException(e, sys)
        
    def initiate_data_transformation(self):
        logging.info("Entered initiate_data_transformation method of Data Transformation class")
        try:
            logging.info("Started data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df  = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_df  = train_df.drop(TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            input_feature_test_df  = test_df.drop(TARGET_COLUMN, axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature  = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr  = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, 
                                  array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,
                                  array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)
            save_object("final_model/preprocessor.pkl", preprocessor_obj)
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path  = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path   = self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
            
        except Exception as e:
            raise ETLPipelineException(e, sys)
        
