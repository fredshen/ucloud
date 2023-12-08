#!/usr/bin/env python3

from ucloud.core import exc
from ucloud.client import Client
import time

#修改为个人秘钥
#账号：shenchaook@gmail.com
Pubulic_Key = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
Private_Key = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"

#基础信息配置
UDPN_ID = "udpn-r3qv8h1dkau"


client = Client({
	"region": "cn-bj2",
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": "org-fye3q5",
	"base_url": "https://api.ucloud.cn"
})

#获取带宽值
resp1 = client.udpn().describe_udpn({
	"UDPNId": UDPN_ID,
	"Limit": 1000
})
Current_Bandwith = resp1.get("DataSet")[0].get("Bandwidth")

#print("------------------1-------------------")
#print(Current_Bandwith)
#print("------------------1-------------------")

#获取监控值
resp2 = client.invoke("GetMetric", {
	"Region": "cn-gd",
	"Zone": "cn-gd-02",
	"ProjectId": "org-fye3q5",
	"ResourceType": "udpn",
	"ResourceId": UDPN_ID,
	"TimeRange": 200,
	"MetricName.0": "BandOutMaxUsage"
})
Current_Bandwith_Usage = resp2.get("DataSets").get("BandOutMaxUsage")[-1].get("Value")
#print(Current_Bandwith_Usage)

if Current_Bandwith_Usage < 60:
	New_Bandwith = int(Current_Bandwith * 0.8)
	if New_Bandwith < 2:
		New_Bandwith = 2
	else:
		New_Bandwith = New_Bandwith *1
elif Current_Bandwith_Usage > 60 and Current_Bandwith_Usage < 80:
	New_Bandwith = int(Current_Bandwith * 0.9)
	if New_Bandwith < 2:
		New_Bandwith = 2
	else:
		New_Bandwith = New_Bandwith *1
else:
	New_Bandwith = int(Current_Bandwith * Current_Bandwith_Usage *1.2 / 100 + 1)
	
#调整带宽值

resp3 = client.udpn().modify_udpn_bandwidth({
		"UDPNId": "udpn-r3qv8h1dkau",
		"Bandwidth": New_Bandwith
})
print("---aaaa----")
print("当前带宽使用率："+ str(Current_Bandwith_Usage))
print("当前带宽购买值："+ str(Current_Bandwith))
print("新购买值："+str(New_Bandwith))
		