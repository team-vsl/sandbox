from pydantic import BaseModel, Field
from typing import Optional, List


class Terms(BaseModel):
    usage: Optional[str] = Field(
        None,
        description="The usage describes the way the data is expected to be used. Can contain business and technical information."
    )
    limitations: Optional[str] = Field(
        None,
        description="The limitations describe the restrictions on how the data can be used, can be technical or restrictions on what the data may not be used for."
    )
    policy: Optional[List[str]] = Field(
        None,
        description="A list of policies, licenses, standards, that are applicable for this data contract and that must be acknowledged by data consumers."
    )
    noticePeriod: Optional[str] = Field(
        None,
        description="The period of time that must be given by either party to terminate or modify a data usage agreement. Uses ISO-8601 period format, e.g., P3M for a period of three months."
    )

