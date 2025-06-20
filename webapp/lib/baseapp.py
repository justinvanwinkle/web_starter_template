import logging

from werkzeug.wrappers import Request, Response
from werkzeug.utils import cached_property
from werkzeug.exceptions import NotFound, MethodNotAllowed

logger = logging.getLogger(__name__)


class BaseApp:
    def __init__(self, url_map_maker):
        self._url_map_maker = url_map_maker

    def __call__(self, environ, start_response):
        try:
            urls = self.url_map.bind_to_environ(environ)
            endpoint, args = urls.match()
            request = Request(environ)
            args["req"] = request
            response = endpoint(**args)
        except NotFound:
            logger.warning(f"404 Not Found: {environ.get('PATH_INFO')}")
            response = Response("Not Found", status=404, mimetype="text/plain")
        except MethodNotAllowed:
            logger.warning(
                f"405 Method Not Allowed: {environ.get('REQUEST_METHOD')} {environ.get('PATH_INFO')}"
            )
            response = Response("Method Not Allowed", status=405, mimetype="text/plain")
        except Exception as e:
            logger.exception(f"500 Internal Server Error: {e}")
            response = Response(
                "Internal Server Error", status=500, mimetype="text/plain"
            )

        return response(environ, start_response)

    @cached_property
    def url_map(self):
        return self._url_map_maker()
