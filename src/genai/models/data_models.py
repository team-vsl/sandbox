from pydantic import BaseModel, Field
from typing import Dict, Optional, Any, List


class BaseQualityCheck(BaseModel):
    type: Optional[str] = Field(None, description="The type of quality check, must be \"sql\"")
    description: Optional[str] = Field(None, description="A human-readable explanation of the check.")


class SQLCheck(BaseQualityCheck):
    type: Optional[str] = Field(default_factory="sql", description="The type of quality check.")
    query: str = Field(..., description="The SQL query used to validate the data.")
    expectedResult: Optional[str] = Field(None, description="Expected result of the query.")
    dialect: Optional[str] = Field(None, description="The SQL dialect that is used for the query. Should be compatible to the server type. Examples: postgres, spark, bigquery, snowflake, duckdb, …")


class FieldDef(BaseModel):
    description: Optional[str] = Field(None, description="An optional string describing the semantic of the data in this field.")
    type: str = Field(None, description="The logical data type of the field.")
    title: Optional[str] = Field(None, description="An optional string providing a human readable name for the field. Especially useful if the field name is cryptic or contains abbreviations.")
    enum: Optional[List[str]] = Field(None, description="A value must be equal to one of the elements in this array value. Only evaluated if the value is not null.")
    required: Optional[bool] = Field(None, description="An indication, if this field must contain a value and may not be null. Default: false")
    primaryKey: Optional[bool] = Field(None, description="If this field is a primary key. Default: false")
    references: Optional[str] = Field(None, description="The reference to a field in another model. E.g. use ‘orders.order_id’ to reference the order_id field of the model orders. Think of defining a foreign key relationship.")
    unique: Optional[bool] = Field(None, description="An indication, if the value must be unique within the model. Default: false")
    example: Optional[List[Any]] = Field(None, description="A list of example values.")
    pii: Optional[bool] = Field(None, description="An indication, if this field contains Personal Identifiable Information (PII).")
    classification: Optional[str] = Field(None, description="The data class defining the sensitivity level for this field, according to the organization’s classification scheme. Examples may be: sensitive, restricted, internal, public.")
    fields: Optional[Dict[str, 'FieldDef']] = Field(None, description="The nested fields (e.g. columns) of the object, record, or struct. Use only when type is object, record, or struct.")
    quality: Optional[List[SQLCheck]] = Field(None,description="Specifies the quality attributes on field level.")


class ModelDef(BaseModel):
    type: Optional[str] = Field(None, description="	The type of the model. Examples: table, view, object. Default: table")
    description: Optional[str] = Field(None, description="An string describing the data model.")
    title: Optional[str] = Field(None, description="An optional string for the title of the data model. Especially useful if the name of the model is cryptic or contains abbreviations.")
    fields: Optional[Dict[str, FieldDef]] = Field(None, description="The fields (e.g. columns) of the data model.")
    quality: Optional[List[SQLCheck]] = Field(None, description="Specifies the quality attributes on model level.")
    

class DataContractModels(BaseModel):
    data_models: Dict[str, ModelDef]
