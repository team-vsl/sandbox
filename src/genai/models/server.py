from pydantic import BaseModel, Field
from typing import Literal, Optional, List


from typing import Literal, List, Optional
from pydantic import BaseModel, Field


class ServerRole(BaseModel):
    name: str = Field(..., description="Name of the role.")
    description: Optional[str] = Field(None, description="A description of the role and what access the role provides.")


class Server(BaseModel):
    type: Literal["s3", "redshift"] = Field(..., description="The type of the data product technology that implements the data contract.")
    description: str
    environment: Literal["prod", "sit", "stg", "dev"] = Field(..., description="Describing the environment.")
    role: List[ServerRole]


class RedshiftServer(Server):
    type: Literal["s3", "redshift"] = "redshift"
    account: str
    database: str
    redshift_schema: str = Field(..., description='schema')
    clusterIdentifier: str = Field(..., description="Identifier of the cluster. Example: analytics-cluster.")
    host: str = Field(..., description="Host of the cluster. Example: analytics-cluster.example.eu-west-1.redshift.amazonaws.com.")
    port: int = Field(..., description="Port of the cluster. Example: 5439")
    endpoint: str = Field(..., description="Endpoint of the cluster. Example: analytics-cluster.example.eu-west-1.redshift.amazonaws.com:5439/analytics.")


class S3Server(Server):
    type: Literal["s3", "redshift"] = "s3"
    location: str = Field(..., description="S3 URL, starting with s3://.")
    endpointUrl: str = Field(..., description="The server endpoint for S3-compatible servers, such as MioIO or Google Cloud Storage, e.g., https://minio.example.com")
    format: str = Field(..., description="Format of files, such as parquet, delta, json, csv")
    delimiter: str = Field(..., description="(Only for format = json), how multiple json documents are delimited within one file, e.g., new_line, array")

    