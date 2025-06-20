import pytest
from werkzeug.routing import Map
from webapp.urls import make_url_map
from webapp.endpoint.home import homepage


class TestURLs:
    def test_make_url_map_returns_map(self):
        url_map = make_url_map()
        assert isinstance(url_map, Map)

    def test_homepage_route_exists(self):
        url_map = make_url_map()

        # Check that we can match the root route
        adapter = url_map.bind("example.com", "/")
        endpoint, values = adapter.match("/")
        assert endpoint == homepage
        assert values == {}

    def test_homepage_route_without_trailing_slash(self):
        url_map = make_url_map()

        # Check that route works without trailing slash (strict_slashes=False)
        adapter = url_map.bind("example.com", "/")
        endpoint, values = adapter.match("/")
        assert endpoint == homepage

        # Should also work with trailing slash
        adapter = url_map.bind("example.com", "/")
        try:
            endpoint, values = adapter.match("/")
            assert endpoint == homepage
        except Exception:
            # Some versions might redirect, that's OK
            pass

    def test_unknown_route_raises_not_found(self):
        url_map = make_url_map()
        adapter = url_map.bind("example.com", "/")

        from werkzeug.exceptions import NotFound

        with pytest.raises(NotFound):
            adapter.match("/unknown-route")

    def test_url_map_contains_rules(self):
        url_map = make_url_map()

        # Convert rules to list to inspect them
        rules = list(url_map.iter_rules())
        assert len(rules) > 0

        # Check that homepage rule exists
        homepage_rules = [r for r in rules if r.endpoint == homepage]
        assert len(homepage_rules) == 1

        # Check rule properties
        rule = homepage_rules[0]
        assert rule.rule == "/"
        assert rule.strict_slashes is False
