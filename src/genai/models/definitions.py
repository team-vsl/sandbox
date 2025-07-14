from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Any, Dict
from .data_field import DataField


class DefinitionObject(BaseModel):
    type: str = Field(..., description="REQUIRED. The logical data type")
    title: Optional[str] = Field(None, description="The business name of this definition.")
    description: Optional[str] = Field(None, description="Clear and concise explanations related to the domain")
    enum: Optional[List[str]] = Field(None, description="A value must be equal to one of the elements in this array value. " \
    "Only evaluated if the value is not null.")
    format: Optional[Literal["email", "uri", "uuid"]] = Field(None, description="email : A value must be complaint to " \
    "RFC 5321, section 4.1.2. uri : A value must be complaint to RFC 3986. uuid : A value must be complaint to RFC 4122. " \
    "Only evaluated if the value is not null. Only applies to unicode character sequences types ( string , text , varchar ).")
    precision: Optional[int] = Field(38, description="The maximum number of digits in a number. Only applies to numeric " \
    "values. Defaults to 38.")
    scale: Optional[int] = Field(0, description="The maximum number of decimal places in a number. Only applies to " \
    "numeric values. Defaults to 0.")
    minLength: Optional[int] = Field(None, description="A value must greater than, or equal to, the value of this. " \
    "Only applied to unicode character sequences types ( string , text , varchar ).")
    maxLength: Optional[int] = Field(None, description="A value must less than, or equal to, the value of this. " \
    "Only applied to unicode character sequences types ( string , text , varchar ).")
    pattern: Optional[str] = Field(None, description="A value must be valid according to the ECMA-262 regular expression " \
    "dialect. Only evaluated if the value is not null. Only applies to unicode character sequences " \
    "types ( string , text , varchar ).")
    minimum: Optional[float] = Field(None, description="A value of a number must greater than, or equal to, the value " \
    "of this. Only applies to numeric values.")
    exclusiveMinimum: Optional[float] = Field(None, description="A value of a number must greater than the value of this. " \
    "Only applies to numeric values.")
    maximum: Optional[float] = Field(None, description="A value of a number must less than, or equal to, the value of this. " \
    "Only applies to numeric values.")
    exclusiveMaximum: Optional[float] = Field(None, description="A value of a number must less than the value of this. " \
    "Only applies to numeric values.")
    examples: Optional[List[Any]] = Field(None, description="A list of example values.")
    pii: Optional[bool] = Field(None, description="An indication, if this field contains Personal Identifiable " \
    "Information (PII).")
    classification: Optional[str] = Field(None, description="The data class defining the sensitivity level for this " \
    "field, according to the organization's classification scheme. " \
    "Examples may be: sensitive , restricted , internal , public .")
    tags: Optional[List[str]] = Field(None, description="Custom metadata to provide additional context.")
    links: Optional[Dict[str, str]] = Field(None, description="Additional external documentation links.")
    fields: Optional[Dict[str, DataField]] = Field(None, description="The nested fields "
    "(e.g. columns) of the object, record, or struct. Use only when type is object , record , or struct .")