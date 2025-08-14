from dataclasses import dataclass

@dataclass
class DataCollectionArtifact:
    elo_data_resource_url       : str
    match_data_resource_url     : str
    elo_data_update_interval    : str
    match_data_update_interval  : str
    match_data_file_path        : str
    elo_data_file_path          : str

@dataclass
class DataIngestionArtifact:
    trained_file_path   : str
    test_file_path      : str

@dataclass 
class DataValidationArtifact:
    validation_status       : bool
    valid_train_file_path   : str
    valid_test_file_path    : str
    invalid_train_file_path : str
    invalid_test_file_path  : str
    drift_report_file_path  : str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path : str
    transformed_train_file_path  : str
    transformed_test_file_path   : str

@dataclass
class ClassificationMetricArtifact:
    f1_score            : float
    precision_score     : float
    recall_score        : float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path : str
    train_metric_artifact   : ClassificationMetricArtifact
    test_metric_artifact    : ClassificationMetricArtifact