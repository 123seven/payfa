import os
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    PROJECT_NAME: str = Field(default="FastApi", description="Project Name")
    DEBUG: bool = Field(default=False, description="Debug Mode")

    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = Field(
        default=["*"], description="CORS CONF ALLOWED_HOSTS"
    )
    CORS_ALLOWED_METHODS: List[Union[AnyHttpUrl, str]] = Field(
        default=["*"], description="CORS CONF ALLOWED_METHODS"
    )
    CORS_ALLOWED_HEADERS: List[Union[AnyHttpUrl, str]] = Field(
        default=["*"], description="CORS CONF ALLOWED_HEADERS"
    )

    DATABASE_DSN: Optional[str] = Field(
        default=f"sqlite:///{BASE_DIR}/database.db", description="Database URL"
    )
    ORDER_EXPIRED_SECOND: int = Field(default=300, description="ORDER EXPIRED SECOND")

    JWT_SECRET_KEY: str = (
        "02d45q3e064fab6ca2w576c018wqy313n7019f6f0f4caa6cf53b98e0r53d3e7"
    )
    JWT_ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True
        env_file = ".env", "local.env", "test.env", "prod.env"
        env_file_encoding = "utf-8"


settings = Settings()
