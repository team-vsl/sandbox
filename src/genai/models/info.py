from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, List, Any


class Contact(BaseModel):
    name: str
    email: Optional[str]
    url: Optional[str]


class Info(BaseModel):
    title: str = Field(..., description="The title of the data contract.")
    version: str = Field(..., description="The version of the data contract document.")
    status: Literal["proposed", "in development", "active", "deprecated", "retired"] = Field(...)
    description: Optional[str] = None
    owner: Optional[str] = None
    contact: Optional[Contact] = None