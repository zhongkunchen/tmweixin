#!coding: utf-8
__author__ = 'zkchen'
from django.conf import settings


_CONTEXT = {}


def update_context(**kwargs):
    """
    update weixin config(appid, secret, mchid, key, cert path...) in runtime
    """
    _CONTEXT.update(kwargs)


class WeixinConf(object):
    def __init__(self):
        self.conf = settings
        d = {}
        for k in ["APPID", "APPSECRET", "MCHID", "KEY", "SSLKEY_PATH", "SSLCERT_PATH"]:
            v = getattr(self.conf, k, None)
            if v:
                d[k] = v
        update_context(**d)

    def _check_key(self, key):
        assert key in _CONTEXT, u"%s must be set before using" % key
        return _CONTEXT[key]

    CURL_TIMEOUT = 5 * 60

    @property
    def app_id(self):
        return self._check_key("APPID")

    @property
    def app_secret(self):
        return self._check_key("APPSECRET")

    @property
    def mch_id(self):
        return self._check_key("MCHID")

    @property
    def key(self):
        return self._check_key("KEY")

    @property
    def ssl_key_path(self):
        return self._check_key("SSLKEY_PATH")

    @property
    def ssl_cert_path(self):
        return self._check_key("SSLCERT_PATH")


wx_conf = WeixinConf()
