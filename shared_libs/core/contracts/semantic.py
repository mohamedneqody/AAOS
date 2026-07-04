from pydantic import BaseModel, ConfigDict
from typing import List

class Entity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    description: str

class Relationship(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source: str
    target: str
    relation: str

class SemanticModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"
    ontology_version: str = "1.0"
    entities: List[Entity]
    relationships: List[Relationship]
    business_meaning: str
    confidence: float
    reasoning: str
