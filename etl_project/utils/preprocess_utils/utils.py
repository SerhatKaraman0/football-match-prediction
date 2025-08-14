import typing
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 


class PreprocessDataFrame:
    """
    A class for data preprocessing operations such as handling outliers
    and encoding categorical variables.
    """
    def __init__(self):
        pass

    def outlier_thresholds(self, df: pd.DataFrame, col_name: str, q1: float = 0.25, q3: float = 0.75) -> typing.Tuple[float, float]:
        """
        Calculates outlier thresholds for a column using the IQR method.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the column
        col_name : str
            The name of the column to calculate thresholds for
        q1 : float, default=0.25
            The first quartile value
        q3 : float, default=0.75
            The third quartile value
            
        Returns:
        --------
        Tuple[float, float]
            Lower and upper thresholds for outliers
        """
        quartile1 = df[col_name].quantile(q1)
        quartile3 = df[col_name].quantile(q3)

        interquantile_range = quartile3 - quartile1

        up_limit = quartile3 + 1.5 * interquantile_range
        low_limit = quartile1 - 1.5 * interquantile_range
         
        return low_limit, up_limit
    

    def check_outlier(self, df: pd.DataFrame, col_name: str) -> bool:
        """
        Checks if outliers exist in a column.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the column
        col_name : str
            The name of the column to check for outliers
            
        Returns:
        --------
        bool
            True if outliers exist, False otherwise
        """
        low_limit, up_limit = self.outlier_thresholds(df, col_name)

        return bool(df[(df[col_name] > up_limit) | (df[col_name] < low_limit)].any(axis=None))
    

    def grab_outliers(self, df: pd.DataFrame, col_name: str, index: bool = False) -> typing.Optional[pd.Index]:
        """
        Retrieves outliers from a column and optionally returns their indices.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the column
        col_name : str
            The name of the column to retrieve outliers from
        index : bool, default=False
            If True, returns the indices of outliers
            
        Returns:
        --------
        pd.Index or None
            Indices of outliers if index=True, otherwise None
        """
        low, up = self.outlier_thresholds(df, col_name)

        if df[(df[col_name] > up) | (df[col_name] < low)].shape[0] > 10:
            print(df[(df[col_name] > up) | (df[col_name] < low)].head())
        
        else:
            print(df[(df[col_name] > up) | (df[col_name] < low)])
        
        if index:
            outlier_index = df[(df[col_name] > up) | (df[col_name] < low)].index 
            return outlier_index
        
    
    def remove_outlier(self, df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        """
        Removes outliers from a column.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the column
        col_name : str
            The name of the column to remove outliers from
            
        Returns:
        --------
        pd.DataFrame
            Dataframe without outliers
        """
        low, up = self.outlier_thresholds(df, col_name)
        df_without_outliers = df[~((df[col_name] > up) | (df[col_name] < low))]

        return df_without_outliers
    

    def replace_with_thresholds(self, df: pd.DataFrame, variable: str) -> None:
        """
        Replaces outliers with threshold values.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the column (modified in-place)
        variable : str
            The name of the column to replace outliers in
            
        Returns:
        --------
        None
            Modifies the dataframe in-place
        """
        low, up = self.outlier_thresholds(df, variable)
        df.loc[(df[variable] < low), variable] = low
        df.loc[(df[variable] > up), variable] = up
    

    def one_hot_encoder(self, df: pd.DataFrame, categorical_cols: list[str], drop_first: bool = False) -> pd.DataFrame:
        """
        One-hot encodes categorical columns.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the columns to encode
        categorical_cols : list[str]
            List of categorical column names to encode
        drop_first : bool, default=False
            Whether to drop the first category in each feature
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with one-hot encoded columns
        """
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=drop_first)
        return df 

