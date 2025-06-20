from unittest.mock import Mock, patch
from werkzeug.wrappers import Request, Response
from webapp.endpoint.home import homepage


class TestHomepage:
    def test_homepage_returns_response(self):
        # Create a mock request
        mock_request = Mock(spec=Request)

        # Mock the renderer
        with patch("webapp.endpoint.home.renderer") as mock_renderer:
            mock_renderer.render.return_value = "<html><body>Test Page</body></html>"

            response = homepage(mock_request)

            # Check that it returns a Response object
            assert isinstance(response, Response)

    def test_homepage_calls_renderer_with_correct_template(self):
        mock_request = Mock(spec=Request)

        with patch("webapp.endpoint.home.renderer") as mock_renderer:
            mock_renderer.render.return_value = "rendered content"

            homepage(mock_request)

            # Check that renderer was called with the correct template
            mock_renderer.render.assert_called_once_with("html/landing.html")

    def test_homepage_response_content_type(self):
        mock_request = Mock(spec=Request)

        with patch("webapp.endpoint.home.renderer") as mock_renderer:
            mock_renderer.render.return_value = "<html>Test</html>"

            response = homepage(mock_request)

            # Check that the mimetype is set correctly
            assert response.mimetype == "text/html"

    def test_homepage_response_content(self):
        mock_request = Mock(spec=Request)
        expected_content = "<html><body>Welcome to the site!</body></html>"

        with patch("webapp.endpoint.home.renderer") as mock_renderer:
            mock_renderer.render.return_value = expected_content

            response = homepage(mock_request)

            # Check that the response contains the rendered content
            assert response.get_data(as_text=True) == expected_content

    def test_homepage_status_code(self):
        mock_request = Mock(spec=Request)

        with patch("webapp.endpoint.home.renderer") as mock_renderer:
            mock_renderer.render.return_value = "content"

            response = homepage(mock_request)

            # Default status code should be 200
            assert response.status_code == 200
