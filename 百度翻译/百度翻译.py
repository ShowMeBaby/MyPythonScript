# coding=utf-8
import http.client
import hashlib
from urllib import parse
import random
import os
os.system("")
appid = '20180904000202819'  # 你的appid
secretKey = 'cBKZfCtKigNCB4F1RuXF'  # 你的密钥
myurl = '/api/trans/vip/translate'
q = input("输入需要翻译的内容: ")
fromLang = 'auto'
toLang = 'auto'
salt = random.randint(32768, 65536)
sign = appid+q+str(salt)+secretKey
m1 = hashlib.md5()
m1.update(sign.encode(encoding='utf-8'))
sign = m1.hexdigest()
myurl = myurl+'?appid='+appid+'&q=' + \
    parse.quote(q)+'&from='+fromLang+'&to='+toLang + \
    '&salt='+str(salt)+'&sign='+sign
try:
    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)
    response = httpClient.getresponse()
    str = response.read().decode('utf-8')
    str = eval(str)
    for line in str['trans_result']:
        print("\n翻译结果:\n\n\t\033[1;31;40m {} \033[0m".format(line['dst']))
except Exception as e:
    print("\n\n\t\033[1;31;40m {} \033[0m".format("未知错误"))
finally:
    if httpClient:
        httpClient.close()
input("\n按回车退出")
