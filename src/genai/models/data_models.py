from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from data_field import DataField, Quality


class Config(BaseModel):
    pass


class Models(BaseModel):
    type: str = Field(default="table", description="The type of the model. E.g., table, view, object.")
    description: Optional[str] = Field(default=None, description="A description of the data model.")
    title: Optional[str] = None
    fields: Dict[str, DataField]
    primaryKey: Optional[List[str]] = None
    quality: Optional[List[Quality]] = None
    examples: Optional[List[Any]] = None
    additionalFields: Optional[bool] = Field(default=False)
    config: Optional[Config] = None