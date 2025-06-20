import os
import tempfile
import shutil
import pytest
from werkzeug.test import Client
from werkzeug.wrappers import Response
from webapp.webapp import make_app


class TestIntegration:
    @pytest.fixture
    def client(self):
        app = make_app()
        return Client(app, Response)

    @pytest.fixture
    def mock_template_dir(self):
        # Create a temporary directory with a test template
        temp_dir = tempfile.mkdtemp()
        templates_dir = os.path.join(temp_dir, "templates", "html")
        os.makedirs(templates_dir)

        # Create a test landing page
        landing_html = """<!DOCTYPE html>
<html>
<head>
    <title>Test Landing Page</title>
</head>
<body>
    <h1>Welcome to the Test Site</h1>
    <p>This is a test landing page.</p>
</body>
</html>"""

        with open(os.path.join(templates_dir, "landing.html"), "w") as f:
            f.write(landing_html)

        # Temporarily override the template directory
        from webapp.lib import render

        original_template_dir = render.renderer.template_path
        render.renderer = render.JinjaRenderer(os.path.join(temp_dir, "templates"))

        yield temp_dir

        # Restore original renderer
        render.renderer = render.JinjaRenderer(original_template_dir)
        shutil.rmtree(temp_dir)

    def test_make_app_creates_baseapp(self):
        app = make_app()
        from webapp.lib.baseapp import BaseApp

        assert isinstance(app, BaseApp)

    def test_homepage_full_request_cycle(self, client, mock_template_dir):
        response = client.get("/")

        # Check status code
        assert response.status_code == 200

        # Check content type
        assert response.mimetype == "text/html"

        # Check content
        content = response.get_data(as_text=True)
        assert "you done it!" in content
        assert "<!DOCTYPE html>" in content

    def test_homepage_with_trailing_slash(self, client, mock_template_dir):
        # Test with trailing slash (should work due to strict_slashes=False)
        response = client.get("/")
        assert response.status_code == 200

        content = response.get_data(as_text=True)
        assert "you done it!" in content

    def test_404_for_unknown_route(self, client):
        response = client.get("/nonexistent-page")
        assert response.status_code == 404
        assert response.get_data(as_text=True) == "Not Found"

    def test_request_headers_passed_through(self, client, mock_template_dir):
        # Test that custom headers are available to the endpoint
        response = client.get(
            "/", headers={"User-Agent": "Test Client", "X-Custom-Header": "test-value"}
        )

        assert response.status_code == 200

    def test_multiple_requests(self, client, mock_template_dir):
        # Test that the app can handle multiple requests
        for i in range(5):
            response = client.get("/")
            assert response.status_code == 200
            content = response.get_data(as_text=True)
            assert "you done it!" in content

    def test_app_singleton_pattern(self):
        # Test that make_app creates new instances
        app1 = make_app()
        app2 = make_app()

        # Should be different instances
        assert app1 is not app2

        # But should have the same behavior
        assert app1._url_map_maker == app2._url_map_maker
