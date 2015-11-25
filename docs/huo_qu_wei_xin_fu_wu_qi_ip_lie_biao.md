# 基础支持工具接口

## 获取微信api服务器ip列表

获取微信服务器ip列表，用于判断推送信息的来源是否来自微信，而非伪造。

```python
from tmweixin.api import credential

ip_li = credential.get_ip_list()
```


## 获取access_token
```python
from tmweixin.api import credential
credential.get_access_token()
```
*该接口是带缓存的（第一次获取了下一次默认从缓存中读取，缓存有效时间7000s），如果想立刻更新缓存获取新的access_token,则*：

> credential.get_access_token(**force_update=True**)

