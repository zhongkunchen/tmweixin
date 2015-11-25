# tmweixin

tmweixin是基于python django开发的微信开发包，主要包括对微信公众号api和微信回调借口的再包装。

## 获取access_token
```python
from tmweixin.api import credential
credential.get_access_token()
```
*该接口是带缓存的（第一次获取了下一次默认从缓存中读取，缓存有效时间7000s），如果想立刻更新缓存获取新的access_token,则*：

> credential.get_access_token(**force_update=True**)

## 获取openid
```python
rom tmweixin.api import credential

code = "xxx"
credential.OAuth2.get_openid(code)
```

## 获取用户列表
```python
from tmweixin.api import subscriber

for openid in subscriber.subscriber_generator():
    # do something
```
注意：subscriber.subscriber_generator() 返回的是一个生成器，迭代获取用户openid列表，如果要指定从哪个openid开始可以传入参数：
