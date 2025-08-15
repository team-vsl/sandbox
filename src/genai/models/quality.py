from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Union
from typing import Annotated, Union
from pydantic import Field as PydanticField

class BaseQualityCheck(BaseModel):
    type: str = Field(..., description="The type of quality check.")
    description: Optional[str] = Field(None, description="A human-readable explanation of the check.")


class SQLCheck(BaseQualityCheck):
    type: Literal["sql"]
    query: str = Field(..., description="The SQL query used to validate the data.")
    expectedResult: Optional[str] = Field(None, description="Expected result of the query.")


class DescriptionCheck(BaseQualityCheck):
    type: Literal["description"]
    required: bool = Field(..., description="Indicates whether the field must have a description.")


QualityCheckUnion = Union[SQLCheck, DescriptionCheck]


class DataQuality(BaseModel):
    quality: List[Annotated[QualityCheckUnion, Field(discriminator='type')]] = Field(..., description="")
