#!coding:utf-8
import httplib
import urllib
import urllib2
import cookielib


def make_post_request(website, cookie_path, data):
    # TODO:to learn the opener and request
    post_data = urllib.urlencode(data)
    cj = cookielib.MozillaCookieJar(cookie_path)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    headers = {"User-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    req = urllib2.Request(website, post_data, headers)
    fi = opener.open(req)
    content = fi.read()
    fi.close()
    cj.save(ignore_discard=True, ignore_expires=True)
    print content


def make_get_request(website, cookie_path):
    # TODO:to learn the opener and request
    cj = cookielib.MozillaCookieJar(cookie_path)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    headers = {"User-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    req = urllib2.Request(website, headers)
    fi = opener.open(website)
    content = fi.read()
    fi.close()
    cj.save(ignore_discard=True, ignore_expires=True)
    print content


def send_get(host, path):
    """
    发送一个get请求到指定的host和位置
    """
    webservice = httplib.HTTP(host)
    webservice.putrequest("GET", path)
    webservice.putheader("Host", host)
    webservice.putheader("User-Agent", "python")
    webservice.putheader("Connection", "Keep-Alive")
    webservice.endheaders()
    status_code, status_message, header = webservice.getreply()
    print(status_code)
    print(header)
    print(status_message)
    print(webservice.getfile().read())


def make_msg_send(host, path, msg):
    """
    包装一个微信消息推送到指定的host
    """
    send_tlp = '''
    <xml><Content><![CDATA[%s]]></Content><FromUserName><![CDATA[gh_0767867]]></FromUserName><MsgType><![CDATA[text]]>
    </MsgType><ToUserName><![CDATA[zkchen9998]]></ToUserName><CreateTime>1427191108</CreateTime></xml>
    '''
    message = send_tlp % msg
    webservice = httplib.HTTP(host)
    webservice.putrequest("POST", path)
    webservice.putheader("Host", host)
    webservice.putheader("User-Agent", "Python Post")
    webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
    webservice.putheader("Content-length", "%d" % len(message))
    webservice.endheaders()
    webservice.send(message)
    status_code, status_message, header = webservice.getreply()
    print(status_code)
    print(header)
    print(webservice.getfile().read())

if __name__ == "__main__":
    # 测试主服务的微信应答
    #make_msg_send(host="www.techmars.net", path="/callback/", msg="go")
    make_msg_send(host="127.0.0.1:8000", path="/callback/", msg="?_01")
    #
    #send_get("m.weather.com.cn", path="/mweather15d/101270101.shtml")
