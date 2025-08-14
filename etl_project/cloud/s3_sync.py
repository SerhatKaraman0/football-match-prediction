import os 
import sys
from etl_project.logging.logger import logging
from etl_project.exception.exception import ETLPipelineException


class S3Sync:
    def sync_folder_to_s3(self,folder, aws_bucket_url):
        try:
            command = f"aws s3 sync {folder} {aws_bucket_url} "
            os.system(command)
            logging.info(f"Folder {folder} synced to {aws_bucket_url}")
        except Exception as e:
            raise ETLPipelineException(e,sys)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        try:
            command = f"aws s3 sync {aws_bucket_url} {folder} "
            os.system(command)
            logging.info(f"Folder {aws_bucket_url} synced to {folder}")
        except Exception as e:
            raise ETLPipelineException(e, sys)
        

if __name__ == "__main__":
    s3_sync = S3Sync()
