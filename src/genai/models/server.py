from typing import Literal, Optional, List, Dict
from pydantic import BaseModel, Field

class ServerRole(BaseModel):
    name: Optional[str] = Field(None, description="Name of the role.")
    description: Optional[str] = Field(
        None,
        description="Description of the role and what access it provides."
    )

class Server(BaseModel):
    type: Optional[Literal["s3", "redshift"]] = Field(None, description="Type of server.")
    description: Optional[str] = Field(None, description="Description of the server.")
    environment: Optional[Literal["prod", "sit", "stg", "dev"]] = Field(
        None,
        description="Environment identifier."
    )
    roles: Optional[List[ServerRole]] = Field(None, description="Access roles for this server.")

class RedshiftServer(Server):
    type: Literal["redshift"] = Field("redshift")
    account: Optional[str] = Field(None, description="AWS account ID hosting the cluster.")
    database: Optional[str] = Field(None, description="Database name.")
    redshift_schema: Optional[str] = Field(None, alias="redshift_schema", description="Schema name.")
    clusterIdentifier: Optional[str] = Field(None, description="Identifier of the cluster.")
    host: Optional[str] = Field(None, description="Cluster host name.")
    port: Optional[int] = Field(None, description="Cluster port, e.g., 5439.")
    endpoint: Optional[str] = Field(None, description="Cluster endpoint URL.")

class S3Server(Server):
    type: Literal["s3"] = Field("s3")
    location: Optional[str] = Field(None, description="S3 URL (e.g., s3://bucket/path).")
    endpointUrl: Optional[str] = Field(
        None, description="Endpoint for S3-compatible server (e.g., MinIO)."
    )
    format: Optional[str] = Field(
        None, description="File format: parquet, delta, csv, json."
    )
    delimiter: Optional[str] = Field(
        None,
        description="Delimiter for multi-document JSON (e.g., new_line, array)."
    )

# Discriminated union
from typing import Annotated, Union
from pydantic import Field as PydanticField

ServerUnion = Annotated[
    Union[RedshiftServer, S3Server],
    PydanticField(discriminator="type")
]

class DataServer(BaseModel):
    server: Dict[str, ServerUnion]