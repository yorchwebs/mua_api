"""Configuration settings for the application."""

from decouple import config


class Config:
    MAILERLITE_API_KEY = config("MAILERLITE_API_KEY")
    MAILERLITE_GROUP_ID = config("MAILERLITE_GROUP_ID", cast=int)
