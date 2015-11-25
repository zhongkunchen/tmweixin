#!coding:utf-8
__author__ = 'akun'
import threading


class Singleton(object):
    """单例模式"""
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    impl = cls.configure() if hasattr(cls, "configure") else cls
                    instance = super(Singleton, cls).__new__(impl, *args, **kwargs)
                    instance.__init__(*args, **kwargs)
                    cls._instance = instance
        return cls._instance
