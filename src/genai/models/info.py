from pydantic import BaseModel, Field
from typing import Optional


class Contact(BaseModel):
    name: Optional[str] = Field(None, description="The identifying name of the contact person/organization.")
    email: Optional[str] = Field(None, description="The email address of the contact person/organization. This MUST be in the form of an email address.")
    url: Optional[str] = Field(None, description="The URL pointing to the contact information. This MUST be in the form of a URL.")


class MetaInfo(BaseModel):
    title: Optional[str] = Field(None, description="The title of the data contract.")
    description: Optional[str] = Field(None, description="A description of the data contract.")
    owner: Optional[str] = Field(None, description="The owner or team responsible for managing the data contract and providing the data.")
    contact: Optional[Contact] = Field(None, description="Contact information for the data contract.")