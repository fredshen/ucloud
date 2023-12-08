#!/usr/bin/env python3


from ucloud.core import exc
from ucloud.client import Client
import time

#修改为个人秘钥
#账号：shenchaook@gmail.com
pubulicKey = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
privateKey = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"








'''
gz:
106.75.148.6/10.13.182.248
hk:
118.193.43.181/10.7.123.156

getmetric
参数	描述信息	单位
BandOut	出带宽	b/s
BandOutMax	峰值出带宽	b/s
BandOutUsage	带宽使用率	％
BandOutMaxUsage	峰值带宽使用率	％
'''

Current_Bandwith = 2
#当前购买带宽值
New_Bandwith = 3
#新的购买带宽值
Current_Bandwith_Usage = 60
#当前带宽使用率
Modification_Range = 15

Log_Path = "/Users/fredshen/Downloads/uwork/API_test"

#调整幅度
Band_Out_Max = "1"
Band_Out_Max_Usage = "1"


client = Client({
	"region": "cn-bj2",
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": "org-fye3q5",
	"base_url": "https://api.ucloud.cn"
})

print("------------------1-------------------")
#调整带宽值
resp1 = client.udpn().modify_udpn_bandwidth({
	"UDPNId": "udpn-r3qv8h1dkau",
	"Bandwidth": 2
})

print("------------------1-------------------")
print(resp1)
print("------------------1-------------------")
time.sleep(2)


print("------------------2-------------------")


#获取带宽值
resp1 = client.udpn().describe_udpn({
	"UDPNId": "udpn-r3qv8h1dkau",
	"Limit": 1000
})

Current_Bandwith = resp1.get("DataSet")[0].get("Bandwidth")
print(Current_Bandwith)

