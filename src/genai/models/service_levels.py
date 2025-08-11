from pydantic import BaseModel, Field
from typing import Optional


class Availability(BaseModel):
    description: Optional[str] = Field(None, description="An optional string describing the availability service level.")
    percentage: Optional[str] = Field(None, description="An optional string describing the guaranteed uptime in percent (e.g., 99.9%)")


class Retention(BaseModel):
    description: Optional[str] = Field(None, description="An optional string describing the retention service level.")
    period: Optional[str] = Field(None, description="An optional period of time, how long data is available. Supported formats: Simple duration (e.g., 1 year, 30d) and ISO 8601 duration (e.g, P1Y).")
    unlimited: Optional[bool] = Field(None, description="An optional indicator that data is kept forever.")
    timestampField: Optional[str] = Field(None, description="An optional reference to the field that contains the timestamp that the period refers to.")


class Latency(BaseModel):
    description: Optional[str] = Field(None, description="An optional string describing the latency service level.")
    threshold: Optional[str] = Field(None, description="An optional maximum duration between the source timestamp and the processed timestamp. Supported formats: Simple duration (e.g., 24 hours, 5s) and ISO 8601 duration (e.g, PT24H).")
    sourceTimestampField: Optional[str] = Field(None, description="An optional reference to the field that contains the timestamp when the data was provided at the source.")
    processedTimestampField: str = Field(None, description="An optional reference to the field that contains the processing timestamp, which denotes when the data is made available to consumers of this data contract.")


class Freshness(BaseModel):
    description: Optional[str] = Field(None, description="An optional string describing the freshness service level.")
    threshold: str = Field(None, description="An optional maximum age of the youngest entry. Supported formats: Simple duration (e.g., 24 hours, 5s) and ISO 8601 duration (e.g, PT24H).")
    timestampField: str = Field(None, description="An optional reference to the field that contains the timestamp that the threshold refers to.")


class Frequency(BaseModel):
    description: Optional[str] = Field(None, description="	An optional string describing the frequency service level.")
    type: Optional[str] = Field(None, description="An optional type of data processing. Typical values are batch, micro-batching, streaming, manual.")
    interval: Optional[str] = Field(None, description="Optional. Only for batch: How often the pipeline is triggered, e.g., daily.")
    cron: Optional[str] = Field(None, description="Optional. Only for batch: A cron expression when the pipelines is triggered. E.g., 0 0 * * *")


class Support(BaseModel):
    description: Optional[str] = Field(None, description="An optional string describing the support service level.")
    time: Optional[str] = Field(None, description="An optional string describing the times when support will be available for contact such as 24/7 or business hours only.")
    responseTime: Optional[str] = Field(None, description="An optional string describing the time it takes for the support team to acknowledge a request. This does not mean the issue will be resolved immediately, but it assures users that their request has been received and will be dealt with.")


class Backup(BaseModel):
    description: Optional[str] = Field(None, description="An optional string describing the backup service level.")
    interval: Optional[str] = Field(None, description="An optional interval that defines how often data will be backed up, e.g., daily.")
    cron: Optional[str] = Field(None, description="An optional cron expression when data will be backed up, e.g., 0 0 * * *.")
    recoveryTime: Optional[str] = Field(None, description="An optional Recovery Time Objective (RTO) specifies the maximum amount of time allowed to restore data from a backup after a failure or loss event (e.g., 4 hours, 24 hours).")
    recoveryPoint: Optional[str] = Field(None, description="An optional Recovery Point Objective (RPO) defines the maximum acceptable age of files that must be recovered from backup storage for normal operations to resume after a disaster or data loss event. This essentially measures how much data you can afford to lose, measured in time (e.g., 4 hours, 24 hours).")


class ServiceLevels(BaseModel):
    availability: Optional[Availability] = Field(None, description="The promised uptime of the system that provides the data.")
    retention: Optional[Retention] = Field(None, description="The period how long data will be available.")
    latency: Optional[Latency] = Field(None, description="The maximum amount of time from the source to its destination.")
    freshness: Optional[Freshness] = Field(None, description="The maximum age of the youngest entry.")
    frequency: Optional[Frequency] = Field(None, description="Frequency describes how often data is updated.")
    support: Optional[Support] = Field(None, description="Support describes the times when support will be available for contact.")
    backup: Optional[Backup] = Field(None, description="Backup specifies details about data backup procedures.")
