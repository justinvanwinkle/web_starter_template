import logging

from werkzeug.serving import run_simple

from webapp.lib.baseapp import BaseApp
from webapp.urls import make_url_map
from webapp.config import get_config

# Get configuration
config = get_config()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def make_app():
    app = BaseApp(make_url_map)
    return app


if __name__ == "__main__":
    run_simple(
        config.HOST,
        config.PORT,
        make_app(),
        use_reloader=config.DEBUG,
        use_debugger=config.DEBUG,
    )
else:
    application = make_app()
