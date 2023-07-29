#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""

from ucloud.core import exc
from ucloud.client import Client
import time
import json

#弹性调带宽
'''
功能：
1.通过接口获取：当前带宽值、带宽使用率、
2.条件判断带宽使用率进行带宽调整。
3.打印日志：时间 当前购买带宽值 当前实际带宽值 带宽使用率 此次调整的带宽值

'''


#修改为个人秘钥
#账号：shenchaook@gmail.com
pubulicKey = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
privateKey = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"
projectId = "org-fye3q5"
udpnId = "udpn-lygdi78yzxf"#修改为个人ID
#old_bandwidth = "10000"#随意设置原始值
#bandoutUsage = 100


#获取UDPN当前购买的带宽值
def main():
	client = Client({
	"region": "cn-gd",
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": projectId,
	"base_url": "https://api.ucloud.cn"
})
	
	try:
		resp = client.udpn().describe_udpn({
			"UDPNId": udpnId
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print("step1----------------")
		old_bandwidth = resp.get("DataSet")[0].get("Bandwidth")
		print(old_bandwidth)
		print("----------------")
		
if __name__ == '__main__':
	main()
	
print(old_bandwidth)


#获取UDPN当前峰值带宽使用率
client = Client({
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": projectId,
	"base_url": "https://api.ucloud.cn"
})

try:
	resp = client.invoke("GetMetric", {
		"Region": "cn-gd",
		"Zone": "cn-gd-02",
		"ProjectId": projectId,
		"ResourceType": "udpn",
		"ResourceId": udpnId,
		"TimeRange": 200,
		"MetricName.0": "BandOutMaxUsage"
})
except exc.RetCodeException as e:
	resp = e.json()
	
	#print("----------------")
	#print(resp)
	#print("----------------")
	#print(resp.get("DataSets").get("BandOutMaxUsage")[len(resp.get("DataSets").get("BandOutMaxUsage")) - 1])
	#print("----------------")
print("step2----------------")
print(resp.get("DataSets").get("BandOutMaxUsage")[len(resp.get("DataSets").get("BandOutMaxUsage")) - 1].get("Value"))
bandoutUsage = resp.get("DataSets").get("BandOutMaxUsage")[len(resp.get("DataSets").get("BandOutMaxUsage")) - 1].get("Value")
print("----------------")
#通过使用率计算新带宽


#print(old_bandwidth)

'''	
if bandoutUsage < 40:
	new_bandwidth = int(old_bandwidth * 0.8)
	print(new_bandwidth)
elif 40 <= bandoutUsage < 60:
	new_bandwidth = int(old_bandwidth * 0.9)
	print(new_bandwidth)
elif 60 <= bandoutUsage < 80:
	new_bandwidth = int(old_bandwidth)
	print(new_bandwidth)
else:
	new_bandwidth = int(bandoutUsage/100*old_bandwidth*1.2)
	print(new_bandwidth)
	

#调整带宽
def main():
	client = Client({
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": projectId,
	"base_url": "https://api.ucloud.cn"
})
	
	try:
		resp = client.udpn().modify_udpn_bandwidth({
			"UDPNId": udpn-lygdi78yzxf,
			"Bandwidth": new_bandwidth
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
		 
if __name__ == '__main__':
	main()
'''