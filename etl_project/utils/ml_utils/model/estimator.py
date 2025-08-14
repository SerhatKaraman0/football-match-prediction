import os
import sys
from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

class ETLModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model        = model
        except Exception as e:
            raise ETLPipelineException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise ETLPipelineException(e,sys)