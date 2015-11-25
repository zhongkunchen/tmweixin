#!coding: utf-8
__author__ = 'zkchen'
import urllib

from tmweixin.conf import wx_conf
from tmweixin.api.base import SimpleApi, CacheResultApi
from tmweixin.api.base import LazyString

ACCESS_TOKEN_CACHE_KEY = "_weixin_access"
SERVER_LIST_CACHE_KEY = "_weixin_server_list"


class AccessToken(CacheResultApi, SimpleApi):
    cache_key = ACCESS_TOKEN_CACHE_KEY
    cache_time = 7000
    data_key = "access_token"

    def __init__(self):
        api_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' \
                  % (wx_conf.app_id, wx_conf.app_secret)
        super(AccessToken, self).__init__(api_url=api_url, data_key=self.data_key)

    def get_access_token(self, force_update=False):
        return self.get_data(force_update=force_update)


class ServerList(CacheResultApi, SimpleApi):
    """  获取微信服务器ip地址列表  """
    cache_time = 7 * 24 * 60 * 60
    cache_key = SERVER_LIST_CACHE_KEY
    data_key = "ip_list"

    success_key = (data_key,)
    api_url = LazyString("https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s",
                         AccessToken().get_access_token)

    def get_ip_list(self):
        return self.get_data()


class OAuth2(CacheResultApi):
    cache_key = "_oauth2_%s"
    cache_time = 7200
    # 获取整个返回字典
    data_key = None

    SNSAPI_BASE = "snsapi_base"
    SNSAPI_USERINFO = "snsapi_userinfo"

    def __init__(self, code):
        super(OAuth2, self).__init__()
        # 每个code分配不同的缓存key
        self.cache_key = self.cache_key % code
        app_id = wx_conf.app_id
        secret = wx_conf.app_secret
        self.api_url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
                       "appid=%(app_id)s&secret=%(secret)s&code=%(code)s" \
                       "&grant_type=authorization_code" % {"app_id": app_id, "secret": secret, "code": code}

    def _check_data(self, result):
        if result.get("errcode") is None:
            return True
        return False

    @classmethod
    def get_openid(cls, code):
        """
        根据code获取用户的openid
        """
        app_id = wx_conf.app_id
        secret = wx_conf.app_secret
        uri = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
              "appid=%(app_id)s&secret=%(secret)s&code=%(code)s&grant_type=authorization_code" % {
                  "app_id": app_id, "secret": secret, "code": code}
        api = SimpleApi.make_api(api_url=uri)
        result = api.get_data()
        return result["openid"]

    @classmethod
    def get_oauth_access_token(cls, code, force_update=False):
        return OAuth2(code).get_data(force_update=force_update)

    @classmethod
    def get_authorize_uri(cls, redirect, scope=None, state="none"):
        if scope is None:
            scope = OAuth2.SNSAPI_BASE
        if scope not in [OAuth2.SNSAPI_BASE, OAuth2.SNSAPI_USERINFO]:
            raise AttributeError(u"scope is invalid")

        url = "https://open.weixin.qq.com/connect/oauth2/authorize?" \
              "appid=%s&redirect_uri=%s&response_type=code&" \
              "scope=%s&state=%s#wechat_redirect" % (wx_conf.app_id, urllib.quote(redirect), scope, state)
        return url


class UserInfo(SimpleApi):
    def __init__(self, openid, oauth_access_token=None):
        """
        :param openid:
        :param oauth_access_token: None 则只能取已关注用户信息
        """
        super(UserInfo, self).__init__()
        if oauth_access_token is None:
            self.api_url = "https://api.weixin.qq.com/cgi-bin/user/info?" \
                           "access_token=%s&openid=%s&lang=zh_CN" % (get_access_token(), openid)
        else:
            self.api_url = "https://api.weixin.qq.com/sns/userinfo?" \
                           "access_token=%s&openid=%s&lang=zh_CN" % (oauth_access_token, openid)

    def _check_data(self, result):
        if result.get("errcode") is None:
            return True
        return False


def get_user_info(openid, oauth_access_token=None):
    """
    Get user info of openid
    :param oauth_access_token:
    - None: Just can get subscribed user's info, return sample
        {
            u'province': u'\u56db\u5ddd',
            u'city': u'\u6210\u90fd',
            u'subscribe_time': 1440990725,
            u'headimgurl': u'http://wx.qlogo.cn/mmopen/PiajxSqBRaEKtvkVVGSNKSNtSaqDBMgBK4TgqPfKCld5N084TygMJCoQkfvc1oJfhicHwhX2KwC2YpYtNN1kvPpA/0',
            u'language': u'zh_CN',
            u'openid': u'oRCuowSlN4UDippCobqt4G1FuxDE',
            u'country': u'\u4e2d\u56fd',
            u'remark': u'',
            u'sex': 2,
            u'subscribe': 1,
            u'nickname': u'\u66f9\u5927\u7490',
            u'groupid': 0
        }

        If openid is a unsubscribed user retuan sample
        {u'subscribe': 0, u'openid': u'oRCuowdjFjN0aMv9wTP4GCCv4t-g'}

    - Not None: Get user info by oauth code, return sample as top one
    """
    return UserInfo(openid, oauth_access_token).get_data()


def get_ip_list():
    """
    Get ip list of weixin api server
    """
    return ServerList().get_ip_list()


def get_access_token():
    """
    Get weixin api access token
    """
    return AccessToken().get_access_token()
