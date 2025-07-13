from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, List, Any


class ServerRole(BaseModel):
    name: str = Field(..., description="Name of the role.")
    description = Optional[str] = Field(..., description="A description of the role and what access the role provides.")


class Server(BaseModel):
    type: Literal["s3", "redshift"] = Field(..., 
    description="The type of the data product technology that implements the data contract.")
    description: str
    environment: Literal["prod", "sit", "stg", "dev"] = Field(..., description="Describing the environment.")
    role: List[ServerRole]