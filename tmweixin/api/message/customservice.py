#!coding:utf-8
"""
@desc 客服接口集
@author zkchen (zhongkunchen@126.com)
"""
import hashlib

from tmweixin.api.base import LazyString, SimpleApi
from tmweixin.api.credential import get_access_token
from tmweixin.api.decorators import pull_api


class KFAccount(object):
    """
    客服帐号接口
    """
    CACHE_KF_LIST_KEY = "_kf_list"
    kf_list_url = LazyString("https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token=%s",
                             get_access_token)
    add_url = LazyString("https://api.weixin.qq.com/customservice/kfaccount/add?access_token=%s", get_access_token)
    update_url = LazyString("https://api.weixin.qq.com/customservice/kfaccount/update?access_token=%s", get_access_token)
    del_url = LazyString("https://api.weixin.qq.com/customservice/kfaccount/del?access_token=%s", get_access_token)

    @pull_api(api_url=kf_list_url, data_key="kf_list")
    def get_kf_list(self, data):
        """ 获取客服列表 """
        return data

    def add_account(self, kf_account, kf_id, nickname, kf_nick=None, password=None):
        """
        添加客服帐号
        :param kf_account: 客服帐号 帐号前缀@公众号微信号
        :param kf_nick: 客服昵称
        :param kf_id: 客服工号
        :param nickname: 客服昵称
        :param password: 32位MD5
        """
        data = locals()
        if data["password"] is not None:
            data["password"] = hashlib.md5(password).hexdigest()

        api = SimpleApi(api_url=self.add_url, post_data=data)
        return api.get_data()

    def update_account(self, kf_account, kf_id=None, nickname=None, kf_nick=None, password=None):
        """
        更新客服帐号
        :param kf_account: 客服帐号 帐号前缀@公众号微信号
        :param kf_nick: 客服昵称
        :param kf_id: 客服工号
        :param nickname: 客服昵称
        :param password: 32位MD5
        """
        data = locals()
        if data["password"] is not None:
            data["password"] = hashlib.md5(password).hexdigest()

        api = SimpleApi(api_url=self.update_url, post_data=data)
        return api.get_data()

    def del_account(self, kf_account):
        """
        删除客服号
        :param kf_account:
        """
        api = SimpleApi(api_url="%s&kf_account=%s" % (self.del_url, kf_account))
        return api.get_data()


