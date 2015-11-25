#!coding=utf-8
from django.db import models
from django.conf import settings

from tmkit.db.virtualdeletion import VirtualDeletionMixin


class DefaultModelMixin(models.Model):
    class Meta:
        abstract = True


MODEL_MIXIN = getattr(settings, "WEIXIN_MODEL_MIXIN", DefaultModelMixin)
assert issubclass(MODEL_MIXIN, models.Model), u"WEIXIN_MODEL_MIXIN must subclass of django.db.models.Model"


class WMenu(MODEL_MIXIN):
    """
    微信菜单
    """
    MENU_TYPE_CHOICES = (('click', u'点击'), ('view', u'查看',), ('parent', u'父菜单'))
    parent = models.ForeignKey('self', verbose_name=u'父菜单', null=True, blank=True, \
                               related_name='children')
    menu_type = models.CharField(u'菜单类型', max_length=10, choices=MENU_TYPE_CHOICES, \
                                 help_text=u'类型为"父菜单",则必须要有子菜单')
    name = models.CharField(u'菜单名称', max_length=20)
    value = models.CharField(u'值', help_text=u'类型为"点击",则输入键码，如果类型为"查看",则输入url', \
                             max_length=256, null=True, blank=True)
    position = models.IntegerField(u'顺序(值越大越靠前）')

    def __unicode__(self):
        return self.name

    def get_children(self):
        return self.children.order_by("-position")

    @classmethod
    def root_nodes(cls):
        return cls.objects.filter(parent=None).order_by('-position')

    class Meta:
        verbose_name = u"微信菜单"
        verbose_name_plural = u"微信菜单管理"


class User(MODEL_MIXIN):
    """
    用户
    """
    SEX_CHOICES = (('1', u'男'), ('0', u'女'), ('2', u'未提交'))
    openid = models.CharField(max_length=50, blank=False, primary_key=True, db_index=True)
    nickname = models.CharField(u'昵称', max_length=50, blank=True, null=True)
    sex = models.CharField(u'性别', choices=SEX_CHOICES, default='2', max_length=10, blank=True, null=True)
    telephone = models.CharField(u'手机号', max_length=11, blank=True, null=True)
    is_active = models.BooleanField(u'是否验证', default=False)
    active_at = models.CharField(u'最新手机验证时间', max_length=50, blank=True, null=True)
    latitude = models.CharField(u'经度', max_length=50, blank=True, null=True)
    longitude = models.CharField(u'纬度', max_length=50, blank=True, null=True)
    precision = models.CharField(u'精度', max_length=50, blank=True, null=True)
    modify_at = models.CharField(u'最新经纬度时间', max_length=50, blank=True, null=True)
    city = models.CharField(u'城市', max_length=100, blank=True, null=True)
    province = models.CharField(u'省份', max_length=100, blank=True, null=True)
    country = models.CharField(u'国家', max_length=100, blank=True, null=True)
    headimgurl = models.URLField(u'用户头像图片地址', blank=True, null=True)
    subscribe_time = models.CharField(u'关注公众账号时间', max_length=50, blank=True, null=True)
    subscribed = models.BooleanField(u'是否关注', default=False)

    def update_with_info(self, userinfo):
        """
        Update user with userinfo
        :param userinfo:
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
        """
        self.nickname = userinfo["nickname"]
        self.sex = str(userinfo["sex"])
        self.city = str(userinfo["city"])
        self.headimgurl = str(userinfo["headimgurl"])
        self.country = str(userinfo["country"])
        if userinfo.get("subscribe") == 1:
            self.subscribed = True
            self.subscribe_time = str(userinfo["subscribe_time"])
        self.save()


    def __unicode__(self):
        return '<%s %s[%s]>' % ("tmweixin.User", self.openid, self.nickname)

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = u"用户管理"


class PayInfoModel(MODEL_MIXIN, VirtualDeletionMixin):
    out_trade_no = models.CharField(u"商户订单编号", max_length=32)
    nonce_str = models.CharField(u"随机字符串", null=True, blank=True, max_length=32)
    sign = models.CharField(u"签名", null=True, blank=True, max_length=32)
    result_code = models.CharField(u"业务结果", null=True, blank=True, max_length=32)
    err_code = models.CharField(u"错误代码", null=True, blank=True, max_length=32)
    err_code_des = models.CharField(u"错误信息描述", null=True, blank=True, max_length=128)
    openid = models.CharField(u"用户标识", null=True, blank=True, max_length=128)
    is_subscribe = models.CharField(u"是否关注公众号", null=True, blank=True, max_length=1)
    trade_type = models.CharField(u"交易类型", null=True, blank=True, max_length=16)
    bank_type = models.CharField(u"付款银行", null=True, blank=True, max_length=16)
    total_fee = models.IntegerField(u"总金额")
    cash_fee = models.IntegerField(u"现金支付金额")
    coupon_count = models.IntegerField(u"代金券或立减优惠使用数量", blank=True, null=True)
    coupon_fee = models.IntegerField(u"代金券或立减优惠使用金额", blank=True, null=True)
    transaction_id = models.CharField(u"微信支付订单号", max_length=32)
    attach = models.CharField(u"商家数据包", null=True, blank=True, max_length=128)
    time_end = models.CharField(u"支付完成时间", max_length=14)

    class Meta:
        verbose_name = u"微信支付结果"
        verbose_name_plural = u"微信支付结果管理"

    def __unicode__(self):
        return "%s:%s" % (self.total_fee, self.time_end)

