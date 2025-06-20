from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response
from werkzeug.test import Client
from webapp.lib.baseapp import BaseApp


def dummy_endpoint(req):
    return Response("Hello, World!")


def endpoint_with_args(req, name):
    return Response(f"Hello, {name}!")


class TestBaseApp:
    def test_init(self):
        def url_map_maker():
            return Map([Rule("/", endpoint=dummy_endpoint)])

        app = BaseApp(url_map_maker)
        assert app._url_map_maker == url_map_maker

    def test_url_map_cached_property(self):
        call_count = 0

        def url_map_maker():
            nonlocal call_count
            call_count += 1
            return Map([Rule("/", endpoint=dummy_endpoint)])

        app = BaseApp(url_map_maker)

        # Access url_map multiple times
        map1 = app.url_map
        map2 = app.url_map
        map3 = app.url_map

        # Should only be called once due to caching
        assert call_count == 1
        assert map1 is map2 is map3

    def test_call_simple_request(self):
        def url_map_maker():
            return Map([Rule("/", endpoint=dummy_endpoint)])

        app = BaseApp(url_map_maker)
        client = Client(app, Response)

        response = client.get("/")
        assert response.status_code == 200
        assert response.get_data(as_text=True) == "Hello, World!"

    def test_call_with_url_parameters(self):
        def url_map_maker():
            return Map([
                Rule("/", endpoint=dummy_endpoint),
                Rule("/hello/<name>", endpoint=endpoint_with_args),
            ])

        app = BaseApp(url_map_maker)
        client = Client(app, Response)

        response = client.get("/hello/Alice")
        assert response.status_code == 200
        assert response.get_data(as_text=True) == "Hello, Alice!"

    def test_request_passed_to_endpoint(self):
        captured_request = None

        def capture_request_endpoint(req):
            nonlocal captured_request
            captured_request = req
            return Response("OK")

        def url_map_maker():
            return Map([Rule("/", endpoint=capture_request_endpoint)])

        app = BaseApp(url_map_maker)
        client = Client(app, Response)

        client.get("/", headers={"X-Test-Header": "test-value"})

        assert captured_request is not None
        assert captured_request.headers.get("X-Test-Header") == "test-value"

    def test_404_for_unknown_route(self):
        def url_map_maker():
            return Map([Rule("/", endpoint=dummy_endpoint)])

        app = BaseApp(url_map_maker)
        client = Client(app, Response)

        response = client.get("/unknown")
        assert response.status_code == 404
        assert response.get_data(as_text=True) == "Not Found"

    def test_method_not_allowed(self):
        def url_map_maker():
            return Map([Rule("/", endpoint=dummy_endpoint, methods=["GET"])])

        app = BaseApp(url_map_maker)
        client = Client(app, Response)

        response = client.post("/")
        assert response.status_code == 405
        assert response.get_data(as_text=True) == "Method Not Allowed"

    def test_500_error_handling(self):
        def error_endpoint(req):
            raise RuntimeError("Test error")

        def url_map_maker():
            return Map([Rule("/", endpoint=error_endpoint)])

        app = BaseApp(url_map_maker)
        client = Client(app, Response)

        response = client.get("/")
        assert response.status_code == 500
        assert response.get_data(as_text=True) == "Internal Server Error"
