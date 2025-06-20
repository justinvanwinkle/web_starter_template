from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import FileSystemBytecodeCache


class JinjaRenderer:
    def __init__(self, template_path, extensions=()):
        self.template_path = str(template_path)
        self._loader = FileSystemLoader(str(template_path))
        self._bytecode_cache = FileSystemBytecodeCache()
        self._environment = Environment(
            loader=self._loader,
            cache_size=-1,
            line_statement_prefix="##",
            extensions=extensions,
            autoescape=True,
            bytecode_cache=self._bytecode_cache,
        )

    def render(self, template_filename, context=None, stream=False):
        if context is None:
            context = {}
        template = self._environment.get_template(template_filename)
        rendered = None
        if stream:
            rendered = template.stream(context)
            rendered.enable_buffering(5)
        else:
            rendered = template.render(context)
        return rendered


_site_content_dir = Path(__file__).parent.parent.parent / "site_content"
_template_dir = _site_content_dir / "templates"

renderer = JinjaRenderer(_template_dir)
