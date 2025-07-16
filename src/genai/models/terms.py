from pydantic import BaseModel, Field
from typing import Optional, List


class Policy(BaseModel):
    name: str
    description: Optional[str]
    url: Optional[str]


class Terms(BaseModel):
    usage: str = Field(..., description="The usage describes the way the data is expected to be used. Can contain business and " \
    "technical information.")
    limitations: str = Field(..., description="The limitations describe the restrictions on how the data can be used, can be " \
    "technical or restrictions on what the data may not be used for.")
    policies: List[Policy] = Field(..., description="A list of policies, licenses, standards, that are applicable for this " \
    "data contract and that must be acknowledged by data consumers.")
    billing: str = Field(..., description="The billing describes the pricing model for using the data, such as whether " \
    "it’s free, having a monthly fee, or metered pay-per-use.")
    notice_period: str = Field(..., description="The period of time that must be given by either party to terminate or " \
    "modify a data usage agreement. Uses ISO-8601 period format, e.g., P3M for a period of three months.")