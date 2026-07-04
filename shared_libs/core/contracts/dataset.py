from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

class DatasetProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    dataset_name: str
    row_count: int
    column_count: int
    columns: List[str]
    data_types: Dict[str, str]
    missing_values: Dict[str, int]
    duplicate_rows: int
    duplicate_percentage: float
    candidate_measures: List[str]
    candidate_dimensions: List[str]
    candidate_time_columns: List[str]
    business_keys: List[str]
    cardinality: Dict[str, int]
    null_ratio: Dict[str, float]
    quality_score: float
    sample_values: Dict[str, List[Any]]
