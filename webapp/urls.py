from werkzeug.routing import Map
from werkzeug.routing import Rule

from webapp.endpoint.home import homepage


def make_url_map():
    return Map([
        Rule("/", endpoint=homepage, strict_slashes=False),
    ])
