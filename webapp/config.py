import os
from dataclasses import dataclass


@dataclass
class Config:
    """Base configuration."""

    DEBUG: bool = False
    HOST: str = "localhost"
    PORT: int = 8080
    LOG_LEVEL: str = "INFO"


@dataclass
class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"


@dataclass
class ProductionConfig(Config):
    """Production configuration."""

    HOST: str = "0.0.0.0"
    LOG_LEVEL: str = "WARNING"


def get_config():
    """Get configuration based on environment."""
    env = os.environ.get("WEBAPP_ENV", "development").lower()

    configs = {
        "development": DevelopmentConfig(),
        "production": ProductionConfig(),
    }

    return configs.get(env, DevelopmentConfig())
