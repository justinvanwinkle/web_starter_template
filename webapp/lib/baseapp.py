# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from werkzeug import cached_property

log = logging.getLogger(__name__)


class BaseApp(object):
    def __init__(self, url_map_maker, al, RequestC):
        self._url_map_maker = url_map_maker
        self.al = al
        self.RequestC = RequestC

    def __call__(self, environ, start_response):
        urls = self.url_map.bind_to_environ(environ)
        endpoint, args = urls.match()
        request = self.RequestC(environ)
        args['req'] = request

        for name in self.al.plugin_names:
            args[name] = self.al.get_plugin(name)

        response = endpoint(**args)
        if request.snookie.should_save:
            log.debug('saving cookie: %s', request.snookie)
            session_data = request.snookie.serialize()
            response.set_cookie('snookie', session_data, httponly=True)

        return response(environ, start_response)

    @cached_property
    def url_map(self):
        return self._url_map_maker()
