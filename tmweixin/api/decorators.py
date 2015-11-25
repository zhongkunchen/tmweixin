#!coding: utf-8
__author__ = 'zkchen'
from base import SimpleApi, CacheResultApi


def pull_api(api_url, data_key, api_klass=None, **kwargs):
    """
    装饰器，用于把一个类实例方法变成pull型api方法
    """
    if api_klass is None:
        api_klass = SimpleApi
    api = api_klass(api_url=api_url, data_key=data_key, **kwargs)

    def wraper(func):
        def inner(self):
            ret = func(self, api.get_data())
            return ret
        return inner
    return wraper


def pull_cache_api(api_url, data_key, cache_time, cache_key, api_klass=None, **kwargs):
    """
    装饰器，用于把一个类实例方法变成带缓存的pull型api方法
    """
    if api_klass is None:
        api_klass = CacheResultApi
    api = api_klass(api_url=api_url, data_key=data_key, cache_key=cache_key, cache_time=cache_time, **kwargs)

    def wraper(func):
        def inner(self):
            ret = func(self, api.get_data())
            return ret
        return inner
    return wraper
