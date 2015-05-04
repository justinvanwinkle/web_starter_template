# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import msgpack
from werkzeug import Request
from werkzeug.utils import cached_property
from werkzeug.contrib.securecookie import SecureCookie

SECRET_KEY = b'n({Em\xe7\x7f\xaf!v\xd6-j\x9f\xf1\x1c\xc6+v\xbc'


class JSONSecureCookie(SecureCookie):
    serialization_method = msgpack


class BaseRequest(Request):
    @cached_property
    def snookie(self):
        data = self.cookies.get('snookie')
        if not data:
            return SecureCookie(secret_key=SECRET_KEY)
        return SecureCookie.unserialize(data, SECRET_KEY)
