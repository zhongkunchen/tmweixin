#!coding: utf-8
__author__ = 'zkchen'
import logging
from functools import wraps
from django.http import HttpResponseForbidden


logger = logging.getLogger(__name__)


def require_wx_user(name="wx_user"):
    def wrapper(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request, name):
                logger.error("require attr %s in request" % name)
                return HttpResponseForbidden()
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return wrapper



