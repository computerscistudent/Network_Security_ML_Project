from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    data_ingestion_dir: str
    feature_store_file_path: str
    train_file_path: str
    test_file_path: str