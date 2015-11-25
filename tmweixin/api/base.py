#!coding:utf-8
import json
import requests
from django.core.cache import cache
from tmweixin.exception import WeixinError, WeixinFault, ClientError
from tmweixin.utils import xml_helper

ERROR_CODE_TOKEN = "errcode"


class LazyString(object):
    def __init__(self, source, *args, **kwargs):
        self._source = source
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        return (self._source % tuple((s() if callable(s) else s for s in self._args))).format(**self._kwargs)


def get_response_text(api_url, post_data=None, is_xml=False, cert=None):
    """
    request api server to get response text, response text is json str or xml format
    :param api_url:
    :param post_data: dict data to send to api server or None
    :param is_xml: format post data to xml if True otherwise json str
    :param cert: cert file path if needed
    """
    assert type(post_data) in [type(None), dict], u"post_data must be dict or None"
    assert type(cert) in [tuple, str, type(None)], u"cert must be tuple, str, or None"

    if post_data is None:
        ret = requests.get(api_url)
    else:
        if is_xml:
            post_data = xml_helper.data_to_xml(post_data)
        else:
            post_data = json.dumps(post_data)
        context = {
            "url": api_url,
            "data": post_data,
        }
        if cert:
            context["cert"] = cert
        ret = requests.post(**context)
    return ret.content


class SimpleApi(object):
    """
    api客户端基类，实现了简单的调用api的方法
    """
    # api地址
    api_url = None
    # 强制从返回的json中检查是否包含data_key并返回，找不到则跑出异常,None则返回完整的json字典
    data_key = None
    # 网络请求时携带的头
    headers = {}
    check_keys = None
    # 错误码
    error_code = {"error_code": 0}
    # 是否需要使用证书
    using_cert = False
    cert = None
    # 是否采用xml格式交互，默认使用json
    is_xml = False

    @classmethod
    def make_api(cls, api_url, post_data=None, is_xml=False, data_key=None, cert=None):
        return cls(api_url=api_url, data_key=data_key, headers=None,
                   post_data=post_data, cert=cert, is_xml=is_xml)

    def __init__(self, api_url=None, data_key=None, headers=None, post_data=None, using_cert=False, is_xml=False,
                 cert=None):
        self.is_xml = is_xml or self.is_xml
        self.using_cert = using_cert or self.using_cert
        self.api_url = api_url or self.api_url
        self.data_key = data_key or self.data_key
        self.headers = headers or self.headers
        self.post_data = post_data
        self.cert = cert or self.cert
        if using_cert and cert is None:
            raise AttributeError(u"using_cert need cert file path")

    def _fetch(self):
        response_text = get_response_text(self.api_url, self.post_data, self.is_xml,
                                          self.using_cert and self.cert or None)
        try:
            if self.is_xml:
                result = xml_helper.xml_to_data(response_text)
            else:
                result = json.loads(response_text)
        except ValueError:
            raise WeixinFault(u"%s" % response_text)
        return result

    def _check_data(self, result):
        """
        检查结果是否正确
        """
        # 对照成功码 ， 都匹配则表示成功
        if type(self.check_keys) is dict:
            for k, v in self.check_keys.items():
                if result.get(k) != v:
                    return False
        # 对照错误码，存在则返回False
        if type(self.error_code) is dict:
            for k, v in self.error_code.items():
                if result.get(k) == v:
                    return False
        return True

    def get_data(self, *args, **kwargs):
        """
        调用接口并返回响应：
        － 使用check_keys(成功码),error_code(错误码)验证结果，非“成功”结果跑出WeixinError
        － 如果设置了 data_key则返回data_key的值
        """
        result = self._fetch()
        if self._check_data(result) is False:
            raise WeixinError(u"error:%s" % str(result), result=result)
        if self.data_key is None:
            return result
        try:
            return result[self.data_key]
        except KeyError:
            raise ClientError(u"%s not in result weixin server return:%s" % (str(self.data_key), str(result)))


class CacheResultApi(SimpleApi):
    """
    使封装的接口能缓存结果
    """
    cache_time = None
    cache_key = None

    def get_data(self, force_update=False):
        """
        @:param force_update:强制更新缓存
        """
        if not all([self.cache_key, self.cache_time]):
            raise NotImplementedError(u"cache_time cache_key should be set")
        data = cache.get(self.cache_key)
        if data is None or force_update:
            result = super(CacheResultApi, self).get_data()
            cache.set(self.cache_key, result, self.cache_time)
            return self.get_data()
        else:
            return data


class WeixinBase(SimpleApi):
    """请求型接口的基类"""

    @classmethod
    def load_kwargs(cls, params, keys, kwargs):
        """
        在kwargs中查找keys序列名的值，并写入字典params中
        :param params:
        :param keys:
        :param kwargs:
        """
        for key in keys:
            if key in kwargs:
                params[key] = kwargs[key]
        return params
