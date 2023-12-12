# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client

#修改为个人秘钥
#账号：1349826830@qq.com
Pubulic_Key = "2DVUfAN0VeWFBIV3OBjn9W9tWB5VqB7iOIN9OVuX7"
Private_Key = "FNoqMqrZqMY5mGpOFeudMzF8EfCtcvq838jVLBmOXavkFzkXlX3NjCE5Mf5OUmrwdf"

#基础信息配置
Package_ID = "bw-qv7mfeyujk3"
UGN_ID = "ugn-qr34zqz4xuh"
Project_ID = "org-en5c1p"

client = Client({
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})

	
#获取当前带宽值
resp1 = client.invoke("GetSimpleUGNBwPackages", {
	"ProjectId": Project_ID,
	"UGNID": UGN_ID
})

Current_Bandwith = resp1.get("BwPackages")[-1].get("BandWidth")
print(Current_Bandwith)

#获取监控值
resp2 = client.invoke("GetMetric", {
	"Region": "cn-sh2",
	"Zone": "cn-sh2-01",
	"ProjectId": "org-en5c1p",
	"ResourceType": "ugnbw",
	"ResourceId": "bw-qv7mfeyujk3",
	"TimeRange": 500,
	"MetricName.0": "UgnBWOutPeakUsage"
})

Current_UgnBWOut_PeakUsage = resp2.get("DataSets").get("UgnBWOutPeakUsage")[-1].get("Value")
print(Current_UgnBWOut_PeakUsage)

#判断
if Current_UgnBWOut_PeakUsage < 60:
	New_Bandwith = int(Current_Bandwith * 0.8)
	if New_Bandwith < 2:
		New_Bandwith = 2
	else:
		New_Bandwith = New_Bandwith *1
elif Current_UgnBWOut_PeakUsage > 60 and Current_UgnBWOut_PeakUsage < 80:
	New_Bandwith = int(Current_Bandwith * 0.9)
	if New_Bandwith < 2:
		New_Bandwith = 2
	else:
		New_Bandwith = New_Bandwith *1
else:
	New_Bandwith = int(Current_Bandwith * Current_UgnBWOut_PeakUsage *1.2 / 100 + 1)
	
#调整带宽值
resp = client.invoke("ModifyUGNBandwidth", {
	"ProjectId": "org-en5c1p",
	"PackageID": "bw-qv7mfeyujk3",
	"UGNID": "ugn-qr34zqz4xuh",
	"BandWidth": New_Bandwith
})

print("---aaaa----")
print("当前带宽使用率："+ str(Current_UgnBWOut_PeakUsage))
print("当前带宽购买值："+ str(Current_Bandwith))
print("新购买值："+str(New_Bandwith))
