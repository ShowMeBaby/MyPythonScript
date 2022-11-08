import requests
import time
import dns.resolver
from ping3 import ping
import eventlet
eventlet.monkey_patch()
Dns_list=['114.114.114.114','8.8.8.8','8.8.4.4','218.102.23.228','211.136.192.6','223.5.5.5','168.126.63.1','168.126.63.2'
,'168.95.1.1','168.95.192.1','203.80.96.9','61.10.0.130','61.10.1.130','208.67.222.222',
'208.67.220.220','202.14.67.4','203.80.96.10','202.14.67.14','198.153.194.1','198.153.192.1'
,'112.106.53.22','168.126.63.1','168.95.192.1','198.153.194.1','210.2.4.8','203.80.96.9','220.67.240.221','84.200.69.80',
'81.218.119.11','180.76.76.76','119.29.29.29']
headerx='http://'
end_url='/30m'
updatedata=""
for i in range(1048576):
    updatedata=updatedata+' '
myobj = {' ':updatedata}
end_up_url='/1m'
nintendoUrl='ctest-dl-lp1.cdn.nintendo.net'
nintendoupUrl='ctest-ul-lp1.cdn.nintendo.net'
headers_up_ua={'user-agent':'Nintendo NX','Content-Type': 'application/x-www-form-urlencoded','host':nintendoupUrl}
headers_dl_ua={'user-agent':'Nintendo NX','host':nintendoUrl}
print("-------------------")
speed_max_dl=0
speed_max_up=0
it_upspeed=0
it_dlspeed=0
fast_Download_server=''
fast_up_server=''
def ping_host(ip):
    ip_address = ip
    response = ping(ip_address)
    if response is not None:
        delay = int(response * 1000)
        print("延迟",delay,'ms')
 
def is_timeout(time_num): # 设置超时时间为 time_num
    def wrap(func):
        def inner(*args, **kwargs):
            try:
                with eventlet.Timeout(time_num, True):
                    func(*args, **kwargs)
                return True
            except eventlet.timeout.Timeout:
                print("速度过慢，跳过")
                print("-------------------")
                return False
            
        return inner
 
    return wrap
 
@is_timeout(30)       
def SpeedCompare(result_really,really_uploadurl):
    T1 = time.time()
    myfile = requests.get(result_really,headers=headers_dl_ua)
    T2 = time.time()
    Downspeed=round(30/(T2 - T1),2)
    print("下载速度",Downspeed,"MB/S")    
    myfile=None
    T1 = time.time()
    x = requests.post(really_uploadurl, data = myobj,headers=headers_dl_ua)
    T2 = time.time()
    Upspeed=round(1/(T2 - T1),2)
    print("上传速度", Upspeed,"MB/S")
    global fast_Download_server,speed_max_dl,speed_max_up,fast_up_server,it_upspeed,it_dlspeed
    if(Downspeed>speed_max_dl):
        speed_max_dl=Downspeed
        fast_Download_server=Download_result.nameserver
        it_upspeed=Upspeed
    if(Upspeed>speed_max_up):
        speed_max_up=Upspeed
        fast_up_server=Upload_result.nameserver
        it_dlspeed=Downspeed
    ping_host(str(Download_IP))
    print("-------------------")
 
for index,dns_server in enumerate(Dns_list):
    Download_result=None
    Upload_result=None
    try:
        myResolver = dns.resolver.Resolver()
        myResolver.nameservers = [dns_server]
        Download_result = myResolver.resolve(nintendoUrl, "A")
        #print(Download_result.rrset)
        Upload_result = myResolver.resolve(nintendoupUrl, "A")
        #print(Upload_result.rrset)
    except:
        print("使用的DNS",dns_server)
        print("DNS无效，跳过")
        print("-------------------")
    if Download_result is not None :
        if Upload_result is not None:
            print("使用的DNS:",Download_result.nameserver)
            Download_IP=Download_result.rrset[0]
            Url_after_Dns_DL=headerx+str(Download_IP)+end_url
            Url_after_Dns_Up=headerx+str(Upload_result.rrset[0])+end_up_url
            #print("解析为",result_really)
            print("开始测速 剩余",len(Dns_list)-index,"个DNS待测试")
            SpeedCompare(Url_after_Dns_DL,Url_after_Dns_Up)       
print('最快下载DNS',fast_Download_server,"下载速度:",speed_max_dl,"MB/S","上传速度",it_upspeed,"MB/S")
print('最快上传DNS',fast_up_server,"下载速度:",it_dlspeed,"MB/S","上传速度:",speed_max_up,"MB/S")
a=input("按任意键退出")