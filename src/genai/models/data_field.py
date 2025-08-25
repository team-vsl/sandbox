from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Any, Dict


class TransformationObject(BaseModel):
    type: Literal["DIRECT", "INDIRECT"] = Field(..., description="Indicates how direct is the relationship " \
    "e.g. in query. Allows values are: DIRECT and INDIRECT.")
    subtype: Optional[
        Literal[
            "IDENTITY", "TRANSFORMATION", "AGGREGATION",
            "JOIN", "GROUP_BY", "FILTER", "SORT", "WINDOW", "CONDITIONAL"
        ]
    ] = Field(
        None,
        description=(
            "Optional. Contains more specific information about the transformation. "
            "Allowed values for type DIRECT : IDENTITY , TRANSFORMATION , AGGREGATION . "
            "Allowed values for type INDIRECT : JOIN , GROUP_BY , FILTER , SORT , WINDOW , CONDITIONAL ."
        )
    )
    description: Optional[str] = Field(None, description="Optional. A string representation of the transformation applied.")
    masking: Optional[bool] = Field(None, description="Optional. Boolean value indicating if the input value was " \
    "obfuscated during the transformation.")


class InputFieldObject(BaseModel):
    namespace: str = Field(..., description="The input dataset namespace, such as the name of the source system or " \
    "the domain of another data contract. Examples: com.example.crm , checkout , snowflake:///{account name}.")
    name: str = Field(..., description="The input dataset name, such as a reference to a data contract, a fully " \
    "qualified table name, a Kafka topic.")
    field: str = Field(..., description="The input field name, such as the field in an upstream data contract, " \
    "a table column or a JSON Path.")
    transformations: Optional[List[TransformationObject]] = Field(None, description="Optional. This describes " \
    "how the input field data was used to generate the final result.")


class LineageObject(BaseModel):
    inputFields: Optional[List[InputFieldObject]] = Field(None, description="The input fields refer to specific fields, " \
    "columns, or data points from source systems or other data contracts that feed into a particular transformation, " \
    "calculation, or final result.")


class ConfigObject(BaseModel):
    avroNamespace: Optional[str] = Field(None, description="(Only on model level) The namespace to use when importing "
    "and exporting the data model from / to Apache Avro.")
    avroType: Optional[str] = Field(None, description="(Only on field level) Specify the field type to use when exporting" \
    " the data model to Apache Avro.")
    avroLogicalType: Optional[str] = Field(None, description="(Only on field level) Specify the logical field type to" \
    " use when exporting the data model to Apache Avro.")
    bigqueryType: Optional[str] = Field(None, description="(Only on field level) Specify the physical column type " \
    "that is used in a BigQuery table, e.g., NUMERIC(5, 2).")
    snowflakeType: Optional[str] = Field(None, description="(Only on field level) Specify the physical column type " \
    "that is used in a Snowflake table, e.g., TIMESTAMP_LTZ.")
    redshiftType: Optional[str] = Field(None, description="(Only on field level) Specify the physical column type " \
    "that is used in a Redshift table, e.g., SMALLINT.")
    sqlserverType: Optional[str] = Field(None, description="(Only on field level) Specify the physical column type " \
    "that is used in a SQL Server table, e.g., DATETIME2.")
    databricksType: Optional[str] = Field(None, description="(Only on field level) Specify the physical column type " \
    "that is used in a Databricks table.")
    glueType: Optional[str] = Field(None, description="(Only on field level) Specify the physical column type " \
    "that is used in an AWS Glue Data Catalog table.")


class DataField(BaseModel):
    description: Optional[str] = Field(None, description="An optional string describing the semantic of the data in this field.")
    type: str = Field(..., description="The logical data type of the field.")
    title: Optional[str] = Field(None, description="An optional string providing a human readable name for the " \
    "field. Especially useful if the field name is cryptic or contains abbreviations.")
    enum: Optional[List[str]] = Field(None, description="A value must be equal to one of the elements in this array value. " \
    "Only evaluated if the value is not null.")
    required: bool = Field(False, description="An indication, if this field must contain a value and may not be null. " \
    "Default: false")
    primaryKey: bool = Field(False, description="If this field is a primary key. Default: false")
    references: Optional[str] = Field(None, description="The reference to a field in another model. " \
    "E.g. use 'orders.order_id' to reference the order_id field of the model orders. Think of defining a " \
    "foreign key relationship.")
    unique: bool = Field(False, description="An indication, if the value must be unique within the model. Default: false")
    format: Optional[Literal["email", "uri", "uuid"]] = Field(None, description="email : A value must be " \
    "complaint to RFC 5321, section 4.1.2. uri : A value must be complaint to RFC 3986. " \
    "uuid : A value must be complaint to RFC 4122. Only evaluated if the value is not null. " \
    "Only applies to unicode character sequences types ( string , text , varchar ).")
    precision: Optional[int] = Field(38, description="The maximum number of digits in a number. Only applies " \
    "to numeric values. Defaults to 38.")
    minLength: Optional[int] = Field(None, description="A value must be greater than, or equal to, the value of this. " \
    "Only evaluated if the value is not null. Only applies to unicode character sequences types ( string , text , varchar ).")
    maxLength: Optional[int] = Field(None, description="A value must less than, or equal to, the value of this. " \
    "Only evaluated if the value is not null. Only applies to unicode character sequences types ( string , text , varchar ).")
    pattern: Optional[str] = Field(None, description="A value must be valid according to the ECMA-262 " \
    "regular expression dialect. Only evaluated if the value is not null. Only applies to unicode character " \
    "sequences types ( string , text , varchar ).")
    minimum: Optional[float] = Field(None, description="A value of a number must greater than, or equal to, the value " \
    "of this. Only evaluated if the value is not null. Only applies to numeric values.")
    exclusiveMinimum: Optional[float] = Field(None, description="A value of a number must greater than the value " \
    "of this. Only evaluated if the value is not null. Only applies to numeric values.")
    maximum: Optional[float] = Field(None, description="A value of a number must less than, or equal to, the value of " \
    "this. Only evaluated if the value is not null. Only applies to numeric values.")
    exclusiveMaximum: Optional[float] = Field(None, description="A value of a number must less than the value of this. " \
    "Only evaluated if the value is not null. Only applies to numeric values.")
    examples: Optional[List[Any]] = Field(None, description="A list of example values.")
    pii: Optional[bool] = Field(None, description="An indication, if this field contains " \
    "Personal Identifiable Information (PII).")
    classification: Optional[str] = Field(None, description="The data class defining the sensitivity level " \
    "for this field, according to the organization's classification scheme. " \
    "Examples may be: sensitive , restricted , internal , public .")
    tags: Optional[List[str]] = Field(None, description="Custom metadata to provide additional context.")
    links: Optional[Dict[str, str]] = Field(None, description="Additional external documentation links.")
    ref: Optional[str] = Field(None, alias="$ref", description="A reference URI to a definition in the " \
    "specification, internally or externally. Properties will be inherited from the definition.")
    fields: Optional[Dict[str, "DataField"]] = Field(None, description="The nested fields (e.g. columns) " \
    "of the object, record, or struct. Use only when type is object , record , or struct .")
    items: Optional["DataField"] = Field(None, description="Describes the type of the elements in the array. " \
    "Use only when type is array .")
    keys: Optional["DataField"] = Field(None, description="Describes the key structure of a map. " \
    "Defaults to type: string if a map is defined as type. Not all server types support different key types. " \
    "Use only when type is map .")
    values: Optional["DataField"] = Field(None, description="Describes the value structure of a map. " \
    "Use only when type is map .")
    lineage: Optional[LineageObject] = Field(None, description="Provides information where the data comes from.")
    config: Optional[ConfigObject] = Field(None, description="Any additional key-value pairs that might be " \
    "useful for further tooling.")