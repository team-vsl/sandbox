from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any


class Config(BaseModel):
    pass


class Quality(BaseModel):
    type: str


class DescriptionTextQuality(Quality):
    type: str = "text"
    description: str


class SQLQuality(Quality):
    type: str = "sql"
    description: str = Field(..., description="A plain text describing the quality of the data.")
    query: str = Field(..., description="A SQL query that returns a single number to compare with the threshold.")
    dialect: str = Field(..., description="The SQL dialect that is used for the query. Should be compatible to the server type. Examples: postgres, spark, bigquery, snowflake, duckdb, …")
    mustBe: Optional[int] = Field(..., description="The threshold to check the return value of the query.")
    mustNotBe: Optional[int] = Field(..., description="The threshold to check the return value of the query.")
    mustBeGreaterThan: Optional[int] = Field(..., description="The threshold to check the return value of the query.")
    mustBeGreaterThanOrEqualTo: Optional[int] = Field(..., description="The threshold to check the return value of the query.")
    mustBeLessThan: Optional[int] = Field(..., description="The threshold to check the return value of the query.")
    mustBeLessThanOrEqualTo: Optional[int] = Field(..., description="The threshold to check the return value of the query.")
    mustBeBetween: Optional[int] = Field(..., description="The threshold to check the return value of the query.")
    mustNotBeBetween: Optional[int] = Field(..., description="The threshold to check the return value of the query.")


class Models(BaseModel):
    type: str = Field(default="table", description="The type of the model. E.g., table, view, object.")
    description: Optional[str] = Field(default=None, description="A description of the data model.")
    title: Optional[str] = None
    fields: Dict[str, Field]
    primaryKey: Optional[List[str]] = None
    quality: Optional[List[Quality]] = None
    examples: Optional[List[Any]] = None
    additionalFields: Optional[bool] = Field(default=False)
    config: Optional[Config] = None