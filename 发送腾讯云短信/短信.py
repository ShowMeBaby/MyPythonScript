from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


# 短信应用 SDK AppID
appid = 1400218547  # SDK AppID 以1400开头

# 短信应用 SDK AppKey
appkey = "44adf34100a957ccbe3426abf5d7255a"

# 需要发送短信的手机号码
phone_numbers = ["13279372760"]

# 短信模板ID，需要在短信控制台中申请
template_id = 346860  # NOTE: 这里的模板 ID`7839`只是示例，真实的模板 ID 需要在短信控制台中申请

# 签名
sms_sign = "哆啦A梦生日网"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是示例，真实的签名需要在短信控制台中申请

sms_type = 0  # Enum{0: 普通短信, 1: 营销短信}
ssender = SmsSingleSender(appid, appkey)
# 每个模版参数 只能有12个字
try:
    result = ssender.send_with_param(86, phone_numbers[0], template_id, [
                                     "一二三四五六七八九十十一", "一二三四五六七八九十十一", "30"], extend="", ext="")
    # result = ssender.send(sms_type, 86, phone_numbers[0],"【腾讯云】您的验证码是: 5678", extend="", ext="")
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)

print(result)
