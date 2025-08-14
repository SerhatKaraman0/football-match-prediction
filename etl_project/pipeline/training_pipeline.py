import os 
import sys
from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.components.data_ingestion import DataIngestion
from etl_project.components.data_validation import DataValidation
from etl_project.components.data_transformation import DataTransformation
from etl_project.components.model_trainer import ModelTrainer
from etl_project.cloud.s3_sync import S3Sync
from etl_project.constants.training_pipeline import TRAINING_BUCKET_NAME
from etl_project.entity.config_entity import (
                                              TrainingPipelineConfig, 
                                              DataIngestionConfig,
                                              DataValidationConfig,
                                              DataTransformationConfig,
                                              ModelTrainerConfig
                                              )
from etl_project.entity.artifact_entity import (
                                                DataTransformationArtifact,
                                                ModelTrainerArtifact,
                                                DataIngestionArtifact,
                                                DataValidationArtifact
                                                )

class TrainingPipeline:
    def __init__(self) -> None:
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()

    def start_data_ingestion(self):
        try:
            logging.info("Data Ingestion started.")
            data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data Ingestion Completed.")
            return data_ingestion_artifact
        except Exception as e:
            raise ETLPipelineException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info("Data Validation started.")
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config  = data_validation_config,
                                            data_ingestion_artifact = data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data Ingestion completed.")
            return data_validation_artifact
        except Exception as e:
            raise ETLPipelineException(e, sys)
    
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            logging.info("Data Transformation started.")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(
                                                    data_transformation_config=data_transformation_config,
                                                    data_validation_artifact=data_validation_artifact
                                                    )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation completed.")
            return data_transformation_artifact        
        except Exception as e:
            raise ETLPipelineException(e, sys)
    
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info("Model Training started.")
            model_training_config = ModelTrainerConfig(self.training_pipeline_config)
            model_training = ModelTrainer(
                                            data_transformation_artifact=data_transformation_artifact,
                                            model_trainer_config=model_training_config
                                        )
            model_training_artifact = model_training.initiate_model_trainer()
            logging.info("Model Training completed.")
            return model_training_artifact
        except Exception as e:
            raise ETLPipelineException(e, sys)
    
 
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise ETLPipelineException(e,sys)
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir, aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise ETLPipelineException(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact         = self.start_data_ingestion()
            data_validation_artifact        = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact    = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact          = self.start_model_training(data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            
            return model_trainer_artifact

        except Exception as e:
            raise ETLPipelineException(e, sys)