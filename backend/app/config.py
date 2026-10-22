"""Application settings shared by the upload service."""

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Typed limits for one in-memory upload attempt."""

    upload_size_limit: int = Field(default=10 * 1024 * 1024, gt=0)
    preview_limit: int = Field(default=100, gt=0)


settings = AppConfig()
