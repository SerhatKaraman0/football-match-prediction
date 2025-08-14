import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 
import seaborn as sns
import os 
import sys
from typing import List
import math

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class VisualizeDataFrame:
    """
    A class for data visualization with various plotting methods for categorical
    and numerical data analysis.
    """
    def __init__(self):
        pass


    def cat_summary(self, df: pd.DataFrame, col_name: str, plot: bool=False) -> None:
        """
        Summarizes categorical columns and optionally plots them.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the column
        col_name : str
            The name of the categorical column to summarize
        plot : bool, default=False
            If True, creates a count plot of the categorical variable
            
        Returns:
        --------
        None
            Prints summary and optionally shows a plot
        """
        print(pd.DataFrame({col_name: df[col_name].value_counts(),
                            "Ratio": 100 * df[col_name].value_counts() / len(df)}))
        
        print("###################################")

        if plot:
            sns.countplot(x=df[col_name], data=df)
            plt.show(block=True)
    

    def num_summary(self, df: pd.DataFrame, numerical_col: str, plot: bool = False) -> None:
        """
        Summarizes numerical columns and optionally plots histograms.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the column
        numerical_col : str
            The name of the numerical column to summarize
        plot : bool, default=False
            If True, creates a histogram of the numerical variable
            
        Returns:
        --------
        None
            Prints summary and optionally shows a plot
        """
        quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
        print(df[numerical_col].describe(quantiles).T)

        if plot:
            df[numerical_col].hist(bins=20)
            plt.xlabel(numerical_col)
            plt.ylabel(numerical_col)
            plt.show(block=True)
            

    def plot_3d(self, df: pd.DataFrame, data_x: str, data_y: str, data_z: str, color: str) -> None:
        """
        Creates 3D scatter plots using plotly.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the columns to plot
        data_x : str
            The name of the column for x-axis
        data_y : str
            The name of the column for y-axis
        data_z : str
            The name of the column for z-axis
        color : str
            The name of the column for color coding
            
        Returns:
        --------
        None
            Displays an interactive 3D plot
            
        Raises:
        -------
        ValueError
            If any of the specified columns are not found in the dataframe
        """
        missing_cols = [col for col in [data_x, data_y, data_z, color] if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Column(s) {', '.join(missing_cols)} not found in the dataframe") 
        
        fig = px.scatter_3d(df, data_x, data_y, data_z, color)
        fig.show()


    def plot_all_histograms(self, df, title_prefix = ""):
        num_cols = df.select_dtypes(include=[np.number]).columns
        n_cols = 3
        n_rows = math.ceil(len(num_cols) / n_cols)
        plt.figure(figsize = (5 * n_cols, 4 * n_rows))
        
        for i, col in enumerate(num_cols, 1): 
            plt.subplot(n_rows, n_cols, i)
            sns.histplot(df[col], kde=True ,bins=30)
            plt.title(f"{title_prefix} {col}")
            plt.xlabel("")
            plt.ylabel("")
        plt.tight_layout ()
        plt.show()
            

    def barplot_maker(self, df: pd.DataFrame, cat_x: str, cat_y: str, title: str) -> None:
        """
        Creates bar plots.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the columns to plot
        cat_x : str
            The name of the column for x-axis
        cat_y : str
            The name of the column for y-axis
        title : str
            The title for the plot
            
        Returns:
        --------
        None
            Displays a bar plot
            
        Raises:
        -------
        ValueError
            If any of the specified columns are not found in the dataframe
        """
        if not cat_x in df.columns or not cat_y in df.columns:
            raise ValueError(f"Column {cat_x} or {cat_y} not found in dataframe")
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=cat_x, y=cat_y, data=df)
        plt.title(title, fontsize=14)
        plt.xlabel(cat_x, fontsize=12)
        plt.ylabel(cat_y, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

    def boxplot_maker(self, df: pd.DataFrame, cat_x: str, cat_y: str) -> None:
        """
        Creates box plots.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the columns to plot
        cat_x : str
            The name of the column for x-axis (categorical)
        cat_y : str
            The name of the column for y-axis (numerical)
            
        Returns:
        --------
        None
            Displays a box plot
        """
        sns.boxplot(data=df, x=cat_x, y=cat_y)
        plt.show()

    def subplot_maker(self, df: pd.DataFrame, num_cols: List[str]) -> None:
        """
        Creates subplots for multiple numerical columns.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the columns to plot
        num_cols : List[str]
            List of numerical column names to create subplots for
            
        Returns:
        --------
        None
            Displays multiple density plots in a subplot grid
        """
        plt.figure(figsize=(20, 25))
        for i in range(0, len(num_cols)):
            plt.subplot(5, 3, i+1)
            sns.kdeplot(x=df[num_cols[i]], color="b", fill=True)
            plt.xlabel(num_cols[i], fontsize=12)
            plt.ylabel('Density', fontsize=12)
            plt.title(num_cols[i], fontsize=14)
            plt.tight_layout()
        plt.show()
    

    def scatterplot_maker(self, df: pd.DataFrame, data_x: str, data_y: str, data_hue: str) -> None:
        """
        Creates scatter plots with hue.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The dataframe containing the columns to plot
        data_x : str
            The name of the column for x-axis
        data_y : str
            The name of the column for y-axis
        data_hue : str
            The name of the column for color coding
            
        Returns:
        --------
        None
            Displays a scatter plot
            
        Raises:
        -------
        ValueError
            If any of the specified columns are not found in the dataframe
        """
        missing_cols = [col for col in [data_x, data_y, data_hue] if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Column(s) {', '.join(missing_cols)} not found in the dataframe")
        
        sns.scatterplot(x=df[data_x], y=df[data_y], hue=df[data_hue])
        plt.show()