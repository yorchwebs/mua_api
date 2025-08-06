"""Schemas for the MUA API."""

from pydantic import BaseModel, EmailStr


class SubscriptionSchema(BaseModel):
    email: EmailStr
