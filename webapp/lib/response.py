# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werkzeug import Response


class BaseResponse(Response):
    def __init__(self, template=None, context=None, renderer=None, **kwargs):
        self.template = template
        self.context = context

        if "mimetype" not in kwargs:
            kwargs["mimetype"] = "text/html"

        if renderer is not None:
            if template is not None:
                kwargs["response"] = renderer(template, context)
            elif template is None:
                kwargs["response"] = renderer(context)

        super(BaseResponse, self).__init__(**kwargs)
