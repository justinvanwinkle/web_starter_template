# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.serving import run_simple
from wsgi_shit import BaseApp
from wsgi_shit import BaseRequest
from dally import AL
from jinja2_helpers import JinjaRenderer


from urls import make_url_map


_static_dir = os.path.join(os.path.dirname(__file__), 'static')
_favicon_fn = os.path.join(_static_dir, 'images', 'favicon.ico')
_template_dir = os.path.join(os.path.dirname(__file__), 'templates')


def make_app():
    al = AL()
    jinja_renderer = JinjaRenderer(_template_dir)
    al.add_plugin('jinja', jinja_renderer)
    app = BaseApp(make_url_map(), al, BaseRequest)
    app = SharedDataMiddleware(
        app,
        {'/static': _static_dir, '/favicon.ico': _favicon_fn})
    return app


port = int(os.environ.get('PORT', 4000))
debug = os.environ.get('DEBUG', 'False') == 'True'


application = make_app()

if debug:
    from werkzeug.debug import DebuggedApplication
    application = DebuggedApplication(application, evalex=True)