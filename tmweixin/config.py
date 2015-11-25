#!coding: utf-8
__author__ = 'zkchen'
from tmkit.runtime_conf import settings as runtime_settings

PATH_EXCLUDE_LIST_TOKEN = runtime_settings.register_key("tmweixin.exclude_path", u"不要求微信环境的页面路径",
                                                        default=["/admin"])
TMWEIXIN_TURN_ON = runtime_settings.register_key("tmweixin.turn_on", u"是否开启微信中间件(True or False)", default=True)
TMWEIXIN_DEBUG = runtime_settings.register_key("tmweixin.debug",
                                               u"是否开启debug模式(True or False)(debug模式下不强制要求获取openid",
                                               default=True)
WEIXIN_TLP_MSG = runtime_settings.register_key("tmweixin.tlp_msg", u"微信默认回复消息", default=u'功能正在上线中，敬请等待')
