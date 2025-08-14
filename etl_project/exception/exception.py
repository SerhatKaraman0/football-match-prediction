import sys
from etl_project.logging import logger

class ETLPipelineException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        try:
            _, _, exc_tb = error_details.exc_info()
        except Exception:
            exc_tb = None

        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = 0
            self.file_name = "NA"

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )
    