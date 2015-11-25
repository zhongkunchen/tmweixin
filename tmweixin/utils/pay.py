#!coding: utf-8
__author__ = 'zkchen'
import hashlib


# ######################### 工具 #########################################
def create_sign(params_map, key, alg=hashlib.md5):
        """
        创建签名:
        第一步，设所有发送或者接收到的数据为集合M，将集合M内非空参数值的参数按照参数名ASCII码从小到大排序（字典序），
        使用URL键值对的格式（即key1=value1&key2=value2…）拼接成字符串stringA。
        特别注意以下重要规则：
         ◆　参数名ASCII码从小到大排序（字典序）；
         ◆　如果参数的值为空不参与签名；
         ◆　参数名区分大小写；
         ◆　验证调用返回或微信主动通知签名时，传送的sign参数不参与签名，将生成的签名与该sign值作校验。
         ◆　微信接口可能增加字段，验证签名时必须支持增加的扩展字段

        第二步，在stringA最后拼接上key=(API密钥的值)得到stringSignTemp字符串，并对stringSignTemp进行MD5运算，再将得到的字符串所有字符转换为大写，得到sign值signValue。
        """
        str_a = (lambda **kwargs: "&".join(sorted(["%s=%s" % (str(k), str(v)) for k, v in kwargs.items()])))(
            **params_map
        )
        str_sign_tmp = "%s&key=%s" % (str_a, key)
        sign = alg(str_sign_tmp).hexdigest().upper()
        return sign


if __name__ == "__main__":
    # ############ test create_sign ##############
    params = {
        "appid": "wxd930ea5d5a258f4f",
        "mch_id": "10000100",
        "device_info": "1000",
        "body": "test",
        "nonce_str": "ibuaiVcKdpRxkhJA",
    }
    mch_key = "192006250b4c09247ec02edce69f6a2d"
    ret = create_sign(params, mch_key)
    assert ret == "9A0A8659F005D6984697E2CA0A9CF3B7", u"fail"
