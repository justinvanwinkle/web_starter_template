import os
from webapp.config import Config, DevelopmentConfig, ProductionConfig, get_config


class TestConfig:
    def test_base_config_defaults(self):
        config = Config()
        assert config.DEBUG is False
        assert config.HOST == "localhost"
        assert config.PORT == 8080
        assert config.LOG_LEVEL == "INFO"

    def test_development_config(self):
        config = DevelopmentConfig()
        assert config.DEBUG is True
        assert config.HOST == "localhost"
        assert config.PORT == 8080
        assert config.LOG_LEVEL == "DEBUG"

    def test_production_config(self):
        config = ProductionConfig()
        assert config.DEBUG is False
        assert config.HOST == "0.0.0.0"
        assert config.PORT == 8080
        assert config.LOG_LEVEL == "WARNING"

    def test_get_config_default(self):
        # Save original env var
        original_env = os.environ.get("WEBAPP_ENV")

        # Test default (development)
        if "WEBAPP_ENV" in os.environ:
            del os.environ["WEBAPP_ENV"]

        config = get_config()
        assert isinstance(config, DevelopmentConfig)
        assert config.DEBUG is True

        # Restore original env var
        if original_env is not None:
            os.environ["WEBAPP_ENV"] = original_env

    def test_get_config_development(self):
        original_env = os.environ.get("WEBAPP_ENV")

        os.environ["WEBAPP_ENV"] = "development"
        config = get_config()
        assert isinstance(config, DevelopmentConfig)
        assert config.DEBUG is True

        # Restore
        if original_env is not None:
            os.environ["WEBAPP_ENV"] = original_env
        else:
            del os.environ["WEBAPP_ENV"]

    def test_get_config_production(self):
        original_env = os.environ.get("WEBAPP_ENV")

        os.environ["WEBAPP_ENV"] = "production"
        config = get_config()
        assert isinstance(config, ProductionConfig)
        assert config.DEBUG is False
        assert config.HOST == "0.0.0.0"

        # Restore
        if original_env is not None:
            os.environ["WEBAPP_ENV"] = original_env
        else:
            del os.environ["WEBAPP_ENV"]

    def test_get_config_unknown_env(self):
        original_env = os.environ.get("WEBAPP_ENV")

        os.environ["WEBAPP_ENV"] = "unknown"
        config = get_config()
        # Should default to development
        assert isinstance(config, DevelopmentConfig)

        # Restore
        if original_env is not None:
            os.environ["WEBAPP_ENV"] = original_env
        else:
            del os.environ["WEBAPP_ENV"]
