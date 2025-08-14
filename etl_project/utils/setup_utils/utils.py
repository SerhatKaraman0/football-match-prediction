import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 


class SetupDataFrame:
    """
    A class for loading datasets from predefined directories.
    """
    def __init__(self):
        """
        Initialize the SetupDataFrame class with base directories for
        data science and machine learning datasets.
        """
        self.DS_BASE_DIR = "/Users/user/Desktop/Projects/data-science/data-ds"
        self.ML_BASE_DIR = "/Users/user/Desktop/Projects/data-science/ml-data"

    def setup_ml(self, file_dir: str) -> pd.DataFrame:
        """
        Loads machine learning datasets from the ml-data directory.
        
        Parameters:
        -----------
        file_dir : str
            The relative path to the file within the ML_BASE_DIR
            
        Returns:
        --------
        pd.DataFrame
            The loaded dataset as a pandas DataFrame
        """
        path = os.path.join(self.ML_BASE_DIR, file_dir)
        df = pd.read_csv(path)
        return df
    
    def setup_ds(self, file_dir: str) -> pd.DataFrame:
        """
        Loads data science datasets from the data-ds directory.
        
        Parameters:
        -----------
        file_dir : str
            The relative path to the file within the DS_BASE_DIR
            
        Returns:
        --------
        pd.DataFrame
            The loaded dataset as a pandas DataFrame
        """
        path = os.path.join(self.DS_BASE_DIR, file_dir)
        df = pd.read_csv(path)
        return df
    