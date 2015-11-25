# openid 与用户


## 一、oauth2认证获取用户信息
获取用户信息需要依次进行以下步骤:
- 1.构造一个认证链接让用户通过微信访问该链接
- 2.获得授权码（code）
- 3.使用code获取oauth_access_token
- 4.使用oauth_access_token拉取用户信息


### 1.认证链接的构造
让用户访问认证链接的目的是为了获得授权码（code）

- 基本授权（SNSAPI_BASE）
- 高级授权（SNSAPI_USERINFO）

⚠：***未订阅用户访问基本授权链接不会弹出授权对话框，访问高级授权则会弹出授权对话框；订阅用户均不会弹出授权对话框；***

构造一般认证链接

```python
from tmweixin.api import credential

credential.OAuth2.get_authorize_uri(redirect="{your redirect path}", scope=credential.OAuth2.SNSAPI_BASE, state="option_arg")
```

构造能拉取用户信息的认证链接

```python
from tmweixin.api import credential

credential.OAuth2.get_authorize_uri(redirect="{your redirect path}", scope=credential.OAuth2.SNSAPI_USERINFO,state="option_arg")
```

### 2.获得授权码
用户访问认证链接后会跳转到由redirect="{your redirect path}"指定的网址，并带着code=xxx
和之前填写的附带信息state="option_arg"

### 3.使用code获取oauth_access_token
```python
from tmweixin.api import credential
code = "xxx"
token = credential.OAuth2.get_oauth_access_token(code)
# 强制更新缓存
token = credential.OAuth2.get_oauth_access_token(code, force_update=False)
```
### 4.拉取用户信息
注意区分订阅用户与非订阅用户的信息获取方式,非订阅用户的信息需要使用`oauth access token` 来获取，而订阅用户只需要`openid`。
```python
from tmweixin.api import credential

# 使用oauth access token 获取用户信息（即使未关注也可以获取）
user_info = credential.get_user_info(openid="xxx", oauth_access_token=token)

# 获取订阅用户信息（如果未关注则返回的信息中只有openid）
user_info = credential.get_user_info(openid="xxx")
```

## 二、获取openid
```python
rom tmweixin.api import credential

code = "xxx"
credential.OAuth2.get_openid(code)
```
***code 为上步中的授权码（code）***

## 三、获取用户列表
```python
from tmweixin.api import subscriber

for openid in subscriber.subscriber_generator():
    # do something
```
注意：subscriber.subscriber_generator() 返回的是一个生成器，迭代获取用户openid列表，如果要指定从哪个openid开始可以传入参数：

> subscriber.subscriber_generator(next_openid)


## 四、设置用户备注
```python
from tmweixin.api import subscriber

ret = subscriber.update_remark("o70XxwEviAM3w7PQNrOZUNktdGmY", "test_remark")
self.assertTrue(ret, u"fail to update remark of user")
```
