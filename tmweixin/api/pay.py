#!coding: utf-8
__author__ = 'zkchen'
import logging
import json
from django.shortcuts import HttpResponse
from django.dispatch import Signal

from tmweixin.utils import xml_helper as util_xml
from base import WeixinBase

from tmweixin.api.base import SimpleApi
from tmweixin.conf import wx_conf
from tmweixin.utils.pay import create_sign
from tmweixin.api import common as com
from tmweixin import signals as sigs

logger = logging.getLogger(__name__)


class UnifiedOrder(WeixinBase):
    """统一下单"""
    data_key = None
    api_url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    is_xml = True
    check_keys = {"result_code": "SUCCESS"}

    def __init__(self, body, out_trade_no, total_fee, spbill_create_ip,
                 notify_url, trade_type, **kwargs):
        super(UnifiedOrder, self).__init__()
        assert trade_type in ["JSAPI", "NATIVE", "APP", "WAP"], u"trade_type error"
        params = {
            "appid": wx_conf.app_id,
            "mch_id": wx_conf.mch_id,
            "out_trade_no": out_trade_no,
            "body": body,
            "total_fee": total_fee,
            "spbill_create_ip": spbill_create_ip,
            "notify_url": notify_url,
            "trade_type": trade_type
        }
        # 根据trade_type 验证参数完备性
        try:
            if params["trade_type"] == "NATIVE":
                params["product_id"] = kwargs["product_id"]
            elif params["trade_type"] == "JSAPI":
                params["openid"] = kwargs["openid"]
        except KeyError as e:
            raise AttributeError(u"参数不足")
        # 如果指定了可选参数则添加
        for attr in ["limit_pay", "goods_tag", "time_start", "time_expire",
                     "fee_type", "attach", "detail", "device_info"]:
            if attr in kwargs:
                params[attr] = kwargs[attr]
        # 创建随机串和签名
        params["nonce_str"] = com.create_nonce_str()
        params["sign"] = create_sign(params, key=wx_conf.key)
        self._params = params
        self.post_data = self._params


class OrderQuery(WeixinBase):
    """订单查询接口"""
    api_url = "https://api.mch.weixin.qq.com/pay/orderquery"
    check_keys = {"result_code": "SUCCESS", "return_code": "SUCCESS"}
    is_xml = True

    def __init__(self, transaction_id=None, out_trade_no=None):
        super(OrderQuery, self).__init__()
        if all([transaction_id is None, out_trade_no is None]):
            raise ValueError(u"out_trade_no and transaction_id is None at same time")
        self._params = {
            "appid": wx_conf.app_id,
            "mch_id": wx_conf.mch_id,
            "nonce_str": com.create_nonce_str(),
        }
        if transaction_id:
            self._params["transaction_id"] = transaction_id
        elif out_trade_no:
            self._params["out_trade_no"] = out_trade_no
        self._params["sign"] = create_sign(self._params, key=wx_conf.key)
        self.post_data = self._params


class CloseOrder(WeixinBase):
    """关闭订单"""
    api_url = "https://api.mch.weixin.qq.com/pay/closeorder"
    check_keys = {"return_code": "SUCCESS"}
    is_xml = True

    def __init__(self, out_trade_no=None):
        super(CloseOrder, self).__init__()
        self._params = {
            "appid": wx_conf.app_id,
            "mch_id": wx_conf.mch_id,
            "nonce_str": com.create_nonce_str(),
            "out_trade_no": out_trade_no
            }
        self._params["sign"] = create_sign(self._params, key=wx_conf.key)
        self.post_data = self._params


class Refund(WeixinBase):
    """退款申请接口"""
    api_url = "https://api.mch.weixin.qq.com/secapi/pay/refund"
    is_xml = True
    using_cert = True
    check_keys = {"return_code": "SUCCESS"}

    def __init__(self, out_refund_no, total_fee, refund_fee, op_user_id=None,
                 transaction_id=None, out_trade_no=None, **kwargs):
        """
        :param out_refund_no: 商户退款单号
        :param total_fee: 总金额
        :param refund_fee: 退款金额
        :param op_user_id: 操作员id（默认为商户号)
        :param transaction_id: 微信订单号
        :param out_trade_no: 商户订单号
        :param kwargs: 其他参数
        :param device_info: 商户自定义终端设备号，如门店号
        :param refund_fee_type: 退款货币类型,默认（CNY）
        > 商户订单号，微信订单号必须至少指定一个
        """
        super(Refund, self).__init__()
        if not any([transaction_id, out_trade_no]):
            raise AttributeError(u"transaction_id , out_trade_no must all be None")
        op_user_id = op_user_id or wx_conf.mch_id
        self._params = {
            "appid": wx_conf.app_id,
            "mch_id": wx_conf.mch_id,
            "nonce_str": com.create_nonce_str(),
            "op_user_id": op_user_id,
            "total_fee": total_fee,
            "out_refund_no": out_refund_no,
            "refund_fee": refund_fee
        }
        if transaction_id:
            self._params["transaction_id"] = transaction_id
        elif out_trade_no:
            self._params["out_trade_no"] = out_trade_no
        self._params = self.load_kwargs(self.post_data, ["device_info", "refund_fee_type"], kwargs)
        self._params["sign"] = create_sign(self._params, key=wx_conf.key)
        self.post_data = self._params


class RefundQuery(WeixinBase):
    """退款查询接口"""
    api_url = "https://api.mch.weixin.qq.com/pay/refundquery"
    is_xml = True
    using_cert = False
    check_keys = {"return_code": "SUCCESS"}

    def __init__(self, transaction_id=None, out_trade_no=None, out_refund_no=None, refund_id=None, **kwargs):
        super(RefundQuery, self).__init__()
        if not any([transaction_id, out_refund_no, out_trade_no, refund_id]):
            raise AttributeError(u"refund_id、out_refund_no、out_trade_no、transaction_id四个参数必填一个")
        self.post_data = {
            "appid": wx_conf.app_id,
            "mch_id": wx_conf.mch_id,
            "nonce_str": com.create_nonce_str(),
        }
        m = [transaction_id, out_refund_no, out_trade_no, refund_id]
        k = "transaction_id, out_refund_no, out_trade_no, refund_id".split(",")
        for name, value in zip(k, m):
            if value:
                self.post_data[name] = value
        self.post_data = self.load_kwargs(self.post_data, ["device_info"], kwargs)
        self.post_data["sign"] = create_sign(self.post_data, key=wx_conf.key)


class DownloadBill(WeixinBase):
    """对账单接口"""
    api_url = "https://api.mch.weixin.qq.com/pay/downloadbill"
    using_cert = False
    is_xml = True
    error_code = {"return_code": "FAIL"}

    def __init__(self, bill_date_str, bill_type=None, **kwargs):
        super(DownloadBill, self).__init__()
        if bill_type not in ["SUCCESS", "REFUND", "REVOKED", "ALL"]:
            raise AttributeError(u"not supported bill_type")
        self.bill_type = bill_type or "ALL"
        self.post_data = {
            "appid": wx_conf.app_id,
            "mch_id": wx_conf.mch_id,
            "nonce_str": com.create_nonce_str(),
            "bill_date": bill_date_str,
            "bill_type": self.bill_type
        }
        self.post_data = self.load_kwargs(self.post_data, ["device_info"], kwargs)
        self.post_data["sign"] = create_sign(self.post_data, key=wx_conf.key)


def pay_notify(request, pay_info_model, **kwargs):
    """
    微信支付后通知接口,如果需要在收到结果后处理业务逻辑，使用以下提供的两个信号
    """
    msg = util_xml.parse_xml_request(request)
    if msg.get("return_code") == "SUCCESS":
        sigs.sig_pay_notify.send(sender=request, msg=msg)
        trade_no, transaction_id = msg.get("out_trade_no"), msg.get("transaction_id")
        if trade_no and transaction_id:
            # 检查是否重复推送
            try:
                pay_info_model.objects.get(transaction_id=transaction_id)
            except pay_info_model.DoesNotExist:
                # 记录微信支付结果
                weixin_pay_info = pay_info_model.objects.create(
                    nonce_str=msg.get("nonce_str"),
                    sign=msg.get("sign"),
                    result_code=msg.get("result_code"),
                    err_code=msg.get("err_code"),
                    err_code_des=msg.get("err_code_des"),
                    openid=msg.get("openid"),
                    is_subscribe=msg.get("is_subscribe"),
                    trade_type=msg.get("trade_type"),
                    bank_type=msg.get("bank_type"),
                    total_fee=int(msg.get("total_fee") or 0),
                    cash_fee=int(msg.get("cash_fee") or 0),
                    coupon_count=int(msg.get("coupon_count") or 0),
                    coupon_fee=int(msg.get("coupon_fee") or 0),
                    transaction_id=(msg.get("transaction_id")),
                    attach=(msg.get("attach")),
                    time_end=(msg.get("time_end")), **kwargs
                )
                weixin_pay_info.save()
                sigs.sig_pay_info_created.send(sender=request, msg=msg, pay_info=weixin_pay_info)
                logger.debug("%s accepted and saved msg:%s" % (transaction_id, msg))
            else:
                logger.error("%s exists in db msg:%s" % (transaction_id, msg))
    return HttpResponse(util_xml.data_to_xml({
        "return_code": "SUCCESS",
        "return_msg": "OK",
        }))


# ######################### 商户支付接口 #############################
class QueryPayInfo(WeixinBase):
    """
    查询付款信息
    """
    using_cert = True
    is_xml = True
    api_url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/gettransferinfo "

    def __init__(self, trade_no):
        super(QueryPayInfo, self).__init__()
        self.partner_trade_no = trade_no


class Pay(WeixinBase):
    """ 向用户付款的api """
    is_xml = True
    using_cert = True
    check_keys = {"return_code": "SUCCESS", "result_code": "SUCCESS"}
    NO_CHECK = "NO_CHECK"  # 不校验真实姓名
    FORCE_CHECK = "FORCE_CHECK"  # 强校验真实姓名
    OPTION_CHECK = "OPTION_CHECK"  # 针对已实名认证的用户才校验真实姓名
    api_url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers"

    def __init__(self, openid, amount, partner_trade_no, desc,
                 check_name=None, re_user_name=None, create_ip="127.0.0.1"):
        super(Pay, self).__init__()
        check_name = check_name or self.OPTION_CHECK
        if all([re_user_name is None, check_name in [self.FORCE_CHECK, self.OPTION_CHECK]]):
            raise AttributeError(u"force_check and option_check require re_user_name")
        defaults = {
            "mch_appid": wx_conf.app_id,
            "mchid": wx_conf.mch_id,
            "nonce_str": com.create_nonce_str(),
            "partner_trade_no": partner_trade_no,
            "openid": openid,
            "check_name": check_name,
            "amount": amount,
            "desc": desc,
            "spbill_create_ip": create_ip,
        }
        if re_user_name:
            defaults["re_user_name"] = re_user_name
        defaults["sign"] = create_sign(defaults, wx_conf.key)
        self.post_data = defaults




