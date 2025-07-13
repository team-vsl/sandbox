from pydantic import BaseModel, Field
from typing import Dict
import models


class DataContract(BaseModel):
    id: str = Field(..., description="An organization-wide unique technical identifier, such as a UUID, URN, slug, string, "
    "or number")
    info: models.Info = Field(..., description="Specifies the metadata of the data contract.")
    server: Dict[str, models.Server] = Field(..., description="Specifies the servers of the data contract.")
    terms: models.Terms = Field(..., description="Specifies the terms and conditions of the data contract.")
    data_models: Dict[str, models.Models]
    definitions: Dict[str, models.Definitions]
    servicelevels: models.ServiceLevels
    tags: Dict[str, str]
