from pydantic import BaseModel, Field
from typing import Optional, Dict


class Availability(BaseModel):
    description: str
    percentage: str


class Retention(BaseModel):
    description: str
    period: str = Field(..., description="An optional period of time, how long data is available. Supported formats: " \
    "Simple duration (e.g., 1 year, 30d) and ISO 8601 duration (e.g, P1Y).")
    unlimited: bool = Field(..., description="An optional indicator that data is kept forever.")
    timestampField: Optional[str] = Field(..., description="An optional reference to the field that contains the timestamp that the period refers to.")


class Latency(BaseModel):
    description: str
    threshold: str = Field(..., description="An optional maximum duration between the source timestamp and the processed timestamp. Supported formats: Simple duration (e.g., 24 hours, 5s) and ISO 8601 duration (e.g, PT24H).")


class ServiceLevels(BaseModel):
    availability: Availability = Field(..., description="The promised uptime of the system that provides the data.")
    retention: Retention = Field(..., description="The period how long data will be available.")
