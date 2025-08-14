import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, fbeta_score, classification_report, confusion_matrix
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from typing import Tuple, Any, Optional
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_validate
from sklearn.utils.multiclass import type_of_target
import xgboost
import warnings
warnings.filterwarnings(action='ignore')


class EvalModel:
    """
    A class for evaluating machine learning models, providing methods for assessing
    both regression and classification models with various metrics.
    
    Usage Examples:
    --------------
    # For automatic detection of problem type
    eval_model = EvalModel()
    eval_model.base_models_auto(X, y)  # Automatically detects if regression or classification
    
    # For specific problem types
    eval_model.base_models(X, y)  # Classification only
    eval_model.base_regression_models(X, y)  # Regression only
    eval_model.base_tree_models(X, y)  # Tree-based models (auto-detects problem type)
    """
    def __init__(self):
        pass

    def eval_regression_model(self, X_test: pd.DataFrame, y_test: pd.Series, model: Any) -> Tuple[float, float, float]:
        """
        Evaluates regression models using R², MAE, and MSE metrics.
        
        Parameters:
        -----------
        X_test : pd.DataFrame
            Test features
        y_test : pd.Series
            Test target values
        model : Any
            Trained regression model with predict method
            
        Returns:
        --------
        Tuple[float, float, float]
            R² score, Mean Absolute Error, Mean Squared Error
        """
        y_pred = model.predict(X_test)
        
        score = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)

        print("R2: ", score, "MSE: ", mse, "MAE: ", mae)

        return score, mae, mse

    def eval_class_model(self, X_test: pd.DataFrame, y_test: pd.Series, model: Any, 
                    visualize: bool = False, beta_param: float = 0.5) -> Tuple[float, float, float, float, float]:
        """
        Evaluates classification models using accuracy, recall, precision, F1, and F-beta scores.
        
        Parameters:
        -----------
        X_test : pd.DataFrame
            Test features
        y_test : pd.Series
            Test target values
        model : Any
            Trained classification model with predict method
        visualize : bool, default=False
            If True, creates a heatmap of the confusion matrix
        beta_param : float, default=0.5
            The beta parameter for F-beta score calculation
            
        Returns:
        --------
        Tuple[float, float, float, float, float]
            Accuracy, recall, precision, F1, and F-beta scores
        """
        y_pred = model.predict(X_test)

        accuracy = float(accuracy_score(y_test, y_pred))
        recall = float(recall_score(y_test, y_pred, average='weighted'))
        precision = float(precision_score(y_test, y_pred, average='weighted'))
        f1 = float(f1_score(y_test, y_pred, average='weighted'))
        f_beta = float(fbeta_score(y_test, y_pred, beta=beta_param, average='weighted'))

        if visualize:
            sns.heatmap(confusion_matrix(y_test, y_pred), annot=True)
            
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))
        
        return accuracy, recall, precision, f1, f_beta
    
    def _is_regression_problem(self, y: pd.Series) -> bool:
        """
        Determines if the target variable represents a regression or classification problem.
        
        Parameters:
        -----------
        y : pd.Series
            Target variable
            
        Returns:
        --------
        bool
            True if regression problem, False if classification problem
        """
        target_type = type_of_target(y)
        return target_type == 'continuous'
    
    def base_models_auto(self, X: pd.DataFrame, y: pd.Series, scoring: Optional[str] = None) -> None:
        """
        Automatically detects problem type and runs appropriate base models.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Features dataframe
        y : pd.Series
            Target variable
        scoring : str, optional
            Scoring metric to use. If None, uses appropriate default for problem type
            
        Returns:
        --------
        None
            Prints cross-validation scores for each model
        """
        if self._is_regression_problem(y):
            print("Detected regression problem...")
            if scoring is None:
                scoring = "neg_mean_squared_error"
            self.base_regression_models(X, y, scoring)
        else:
            print("Detected classification problem...")
            if scoring is None:
                scoring = "roc_auc"
            self.base_models(X, y, scoring)
    
    def base_regression_models(self, X: pd.DataFrame, y: pd.Series, scoring: str = "neg_mean_squared_error") -> None:
        """
        Runs and evaluates multiple base regression models on a dataset.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Features dataframe
        y : pd.Series
            Target variable (continuous)
        scoring : str, default="neg_mean_squared_error"
            Scoring metric to use for evaluation
            
        Returns:
        --------
        None
            Prints cross-validation scores for each model
        """
        print("Base Regression Models...")
        regressors = [
            ('Linear', LinearRegression()),
            ('Ridge', Ridge()),
            ('Lasso', Lasso()),
            ('KNN', KNeighborsRegressor()),
            ('CART', DecisionTreeRegressor()),
            ('RF', RandomForestRegressor()),
            ('AdaBoost', AdaBoostRegressor()),
            ('GBM', GradientBoostingRegressor()),
            ('XGBoost', xgboost.XGBRegressor(eval_metric='rmse')),
        ]

        for name, regressor in regressors:
            try:
                CV_results = cross_validate(regressor, X, y, cv=3, scoring=scoring)
                mean_score = np.mean(CV_results['test_score'])
                if np.isnan(mean_score):
                    print(f"{scoring}: NaN {mean_score} ({name}) - Check if the scoring metric is compatible with this model and data.")
                else:
                    print(f"{scoring}: {round(mean_score, 4)} ({name}) ")
            except Exception as e:
                print(f"{scoring}: Error ({name}) - {e}")

    def base_tree_models(self, X: pd.DataFrame, y: pd.Series, scoring: Optional[str] = None) -> None:
        """
        Runs and evaluates tree-based models, automatically detecting problem type.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Features dataframe
        y : pd.Series
            Target variable
        scoring : str, optional
            Scoring metric to use. If None, uses appropriate default for problem type
            
        Returns:
        --------
        None
            Prints cross-validation scores for each model
        """
        is_regression = self._is_regression_problem(y)
        
        if is_regression:
            print("Tree-based Regression Models...")
            if scoring is None:
                scoring = "neg_mean_squared_error"
            self.base_regression_models(X, y, scoring)
        else:
            print("Tree-based Classification Models...")
            if scoring is None:
                scoring = "roc_auc"
            # Detect multiclass and adjust scoring if needed
            n_classes = len(np.unique(y))
            if scoring == "roc_auc" and n_classes > 2:
                scoring = "roc_auc_ovr"
            models = [
                ('CART', DecisionTreeClassifier()),
                ('RF', RandomForestClassifier()),
                ('AdaBoost', AdaBoostClassifier()),
                ('GBM', GradientBoostingClassifier()),
                ('XGBoost', xgboost.XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
            ]

        for name, model in models:
            try:
                CV_results = cross_validate(model, X, y, cv=3, scoring=scoring)
                print(f"{scoring}: {round(CV_results['test_score'].mean(), 4)} ({name}) ")
            except Exception as e:
                print(f"{scoring}: Error ({name}) - {e}")

    def base_models(self, X: pd.DataFrame, y: pd.Series, scoring: str = "roc_auc") -> None:
        """
        Runs and evaluates multiple base classification models on a dataset.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Features dataframe
        y : pd.Series
            Target variable
        scoring : str, default="roc_auc"
            Scoring metric to use for evaluation
            
        Returns:
        --------
        None
            Prints cross-validation scores for each model
        
        Notes:
        ------
        This method is specifically for classification. For regression, use base_regression_models.
        For automatic detection, use base_models_auto.
        Automatically adjusts scoring for multiclass problems, changing 'roc_auc' to 'roc_auc_ovr'
        """
        # Check if this is actually a regression problem
        if self._is_regression_problem(y):
            print("Warning: Detected continuous target variable. This appears to be a regression problem.")
            print("Consider using base_regression_models() or base_models_auto() instead.")
            return
            
        print("Base Classification Models...")
        classifiers = [
            ('LR', LogisticRegression(max_iter=1000)),
            ('KNN', KNeighborsClassifier()),
            ('SVC', SVC(probability=True)),
            ('CART', DecisionTreeClassifier()),
            ('RF', RandomForestClassifier()),
            ('Adaboost', AdaBoostClassifier()),
            ('GBM', GradientBoostingClassifier()),
            # ('XGBoost', xgboost.XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
            # ('LightGBM', LGBMClassifier()),
            # ('CatBoost', CatBoostClassifier(verbose=False))
        ]

        # Detect multiclass and adjust scoring if needed
        n_classes = len(np.unique(y))
        if scoring == "roc_auc" and n_classes > 2:
            scoring = "roc_auc_ovr"

        for name, classifier in classifiers:
            try:
                CV_results = cross_validate(classifier, X, y, cv=3, scoring=scoring)
                print(f"{scoring}: {round(CV_results['test_score'].mean(), 4)} ({name}) ")
            except Exception as e:
                print(f"{scoring}: Error ({name}) - {e}")






     