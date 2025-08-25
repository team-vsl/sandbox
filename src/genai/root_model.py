from pydantic import BaseModel, Field
from typing import Optional

from .models import Terms, MetaInfo, DataServer, DataContractModels, ServiceLevels

class DataContract(BaseModel):
    id: Optional[str] = Field(
        None, description="Unique identifier for this data contract (URN or slug)"
    )
    metainfo: Optional[MetaInfo] = Field(None, description="General metadata about the data contract")
    servers: Optional[DataServer] = Field(
        None, description="Map of named server entries"
    )
    models: Optional[DataContractModels] = Field(
        None, description="Logical data models defined in this contract"
    )
    terms: Optional[Terms] = Field(None, description="Terms of data usage, limitations, billing")
    servicelevels: Optional[ServiceLevels] = Field(
        None, description="SLA, freshness, retention, backup, etc."
    )