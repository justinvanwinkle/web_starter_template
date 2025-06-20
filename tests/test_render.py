import os
import tempfile
import shutil
import pytest
from webapp.lib.render import JinjaRenderer


class TestJinjaRenderer:
    @pytest.fixture
    def temp_template_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def renderer(self, temp_template_dir):
        return JinjaRenderer(temp_template_dir)

    def test_init(self, temp_template_dir):
        renderer = JinjaRenderer(temp_template_dir)
        assert renderer.template_path == temp_template_dir
        assert renderer._environment.autoescape is True
        assert renderer._environment.line_statement_prefix == "##"
        # cache_size attribute doesn't exist in newer Jinja2 versions

    def test_init_with_extensions(self, temp_template_dir):
        extensions = ["jinja2.ext.do", "jinja2.ext.loopcontrols"]
        renderer = JinjaRenderer(temp_template_dir, extensions=extensions)

        # Check if extensions are loaded
        env_extensions = list(renderer._environment.extensions.keys())
        assert "jinja2.ext.ExprStmtExtension" in env_extensions
        assert "jinja2.ext.LoopControlExtension" in env_extensions

    def test_render_simple_template(self, temp_template_dir, renderer):
        # Create a test template
        template_content = "Hello, {{ name }}!"
        template_path = os.path.join(temp_template_dir, "test.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Render the template
        result = renderer.render("test.html", {"name": "World"})
        assert result == "Hello, World!"

    def test_render_without_context(self, temp_template_dir, renderer):
        # Create a test template without variables
        template_content = "Hello, World!"
        template_path = os.path.join(temp_template_dir, "static.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Render without context
        result = renderer.render("static.html")
        assert result == "Hello, World!"

    def test_render_with_autoescape(self, temp_template_dir, renderer):
        # Create a template to test autoescape
        template_content = "{{ content }}"
        template_path = os.path.join(temp_template_dir, "escape.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Render with HTML content
        result = renderer.render(
            "escape.html", {"content": "<script>alert('xss')</script>"}
        )
        assert result == "&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;"

    def test_render_stream(self, temp_template_dir, renderer):
        # Create a template for streaming
        template_content = "{% for i in range(5) %}Item {{ i }}{% endfor %}"
        template_path = os.path.join(temp_template_dir, "stream.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Render as stream
        stream = renderer.render("stream.html", stream=True)
        result = "".join(stream)
        assert result == "Item 0Item 1Item 2Item 3Item 4"

    def test_line_statement_prefix(self, temp_template_dir, renderer):
        # Create a template using line statement prefix
        template_content = """## if True
Hello
## endif"""
        template_path = os.path.join(temp_template_dir, "line_stmt.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        result = renderer.render("line_stmt.html")
        assert result.strip() == "Hello"

    def test_template_not_found(self, renderer):
        with pytest.raises(Exception):  # Jinja2 raises TemplateNotFound
            renderer.render("nonexistent.html")

    def test_nested_templates(self, temp_template_dir, renderer):
        # Create a base template
        base_content = """<!DOCTYPE html>
<html>
<body>{% block content %}{% endblock %}</body>
</html>"""
        base_path = os.path.join(temp_template_dir, "base.html")
        with open(base_path, "w") as f:
            f.write(base_content)

        # Create a child template
        child_content = """{% extends "base.html" %}
{% block content %}Hello, {{ name }}!{% endblock %}"""
        child_path = os.path.join(temp_template_dir, "child.html")
        with open(child_path, "w") as f:
            f.write(child_content)

        result = renderer.render("child.html", {"name": "Test"})
        assert "Hello, Test!" in result
        assert "<!DOCTYPE html>" in result
