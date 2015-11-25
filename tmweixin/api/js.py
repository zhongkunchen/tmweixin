#!coding: utf-8
__author__ = 'zkchen'
import hashlib
import json
import time

from tmweixin.conf import wx_conf
from base import CacheResultApi
from credential import get_access_token
from tmweixin.utils.pay import create_sign

import common as com


class JsApiTicket(CacheResultApi):
    data_key = 'ticket'
    cache_time = 7200
    cache_key = "_jsapi_ticket"

    def __init__(self):
        super(JsApiTicket, self).__init__()
        token = get_access_token()
        self.api_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token


class Config(object):
    """
    jsapisdk 配置类
    """
    def __init__(self,  url, app_list=None, debug=False):
        self.params = {"debug": debug, "appId": wx_conf.app_id, "timestamp": int(time.time()),
                       "nonceStr": com.create_nonce_str(), "url": url}
        self.params["signature"] = self._create_signature(self.params)
        self.app_list = app_list or []
        self.params["jsApiList"] = self.app_list

    @classmethod
    def get_instance(cls, url, debug=False, app_list=None):
        return Config(url=url, debug=debug, app_list=app_list)

    def as_json(self):
        """
        直接后台生成配置对象
        """
        return json.dumps(self.params)

    @property
    def biz_package(self):
        """
        返回参数包，由前端灵活配置
        """
        return self.params

    @classmethod
    def _create_signature(cls, params):
        params_map = params
        txt = "jsapi_ticket=%(jsapi_ticket)s&noncestr=%(nonceStr)s&timestamp=%(timestamp)s&url=%(url)s" % {
            "jsapi_ticket": JsApiTicket().get_data(),
            "nonceStr": params_map["nonceStr"],
            "timestamp": params_map["timestamp"],
            "url": params_map["url"]
        }
        txt = hashlib.sha1(txt).hexdigest()
        return txt


class JsPay(object):
    """
    微信支付jsjdk接口
    """
    def __init__(self, prepay_id, sign_type="MD5"):
        params = {
            "appId": wx_conf.app_id,
            "timeStamp": int(time.time()),
            "nonceStr": com.create_nonce_str(),
            "package": "prepay_id=%s" % prepay_id,
            "signType": sign_type,
        }
        params["paySign"] = create_sign(params, key=wx_conf.key)
        params['timestamp'] = params["timeStamp"]
        del params['timeStamp']
        self._params = params

    def as_json(self):
        return json.dumps(self._params)

    @property
    def biz_package(self):
        return self._params

