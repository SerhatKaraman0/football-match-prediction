from etl_project.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from etl_project.entity.config_entity import DataValidationConfig
from etl_project.logging.logger import logging
from etl_project.exception.exception import ETLPipelineException
from etl_project.constants.training_pipeline import SCHEMA_FILE_PATH
from etl_project.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp # for checking data drift 
import pandas as pd
import os 
import sys


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, 
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config  = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise ETLPipelineException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ETLPipelineException(e, sys)
        
    def validate_num_of_cols(self, df: pd.DataFrame) -> bool:
        try:
            num_of_cols = len(self._schema_config)
            logging.info(f"Required num of cols: {num_of_cols}")
            logging.info(f"Received num of cols: {len(df.columns)}")

            return len(df.columns) == num_of_cols
        except Exception as e:
            raise ETLPipelineException(e, sys)

    def detect_data_drift(self, base_df, current_df, threshold: float = 0.05) -> bool:
        try:
            status = True
            report = {}

            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]

                is_sample_dist_same = ks_2samp(d1, d2)

                if threshold <= is_sample_dist_same.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({col:{
                    "p_value"     : float(is_sample_dist_same.pvalue),
                    "drift_status": is_found 
                    }})
                
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(drift_report_file_path, report)
            return status

        except Exception as e:
            raise ETLPipelineException(e, sys)

    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = DataValidation.read_data(train_file_path)
            test_df  = DataValidation.read_data(test_file_path)

            status = self.validate_num_of_cols(train_df)
            if not status:
                error_msg = "Train df doesn't contain all the columns"
                logging.error(error_msg)
            
            status = self.validate_num_of_cols(test_df)
            if not status:
                error_msg = "Test df doesn't contain all the columns"
                logging.error(error_msg)

            # check datadrift 
            status = self.detect_data_drift(train_df, test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise ETLPipelineException(e, sys)


