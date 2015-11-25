#!coding: utf-8
__author__ = 'zkchen'
from tmweixin.api.base import WeixinBase


class RedPacket(WeixinBase):
    """ 发红包 """
    url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack"

    def __init__(self, factory, **kwargs):
        super(RedPacket, self).__init__(factory=factory, **kwargs)

    def get_result(self):
        return self.get_result_ssl()
