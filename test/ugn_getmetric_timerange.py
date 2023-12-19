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


Package_ID = "default-bw-rh0c0u3tcs1"
UGN_ID = "ugn-qr34zqz4xuh"
Project_ID = "org-en5c1p"
#Log_Path = "/Users/fredshen/Downloads/uwork/API_test"



client = Client({
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": "Input project ID at here",
	"base_url": "https://api.ucloud.cn"
})

resp = client.invoke("GetMetric", {
	"Region": "cn-sh2",
	"Zone": "cn-sh2-01",
	"ProjectId": Project_ID,
	"ResourceType": "ugnbw",
	"ResourceId": Package_ID,
	"TimeRange": 3000,
	"MetricName.0": "UgnBWOutPeakUsage"
})

print("------------")


Usage_Data = resp["DataSets"].get("UgnBWOutPeakUsage")

Time_Range = []
Frequency = []


for i in range(len(Usage_Data)):
	Time_Range.append(Usage_Data[i].get("Timestamp"))
print("时间戳：")
print (Time_Range)

for a in range(len(Time_Range)-1):
	Frequency.append(Time_Range[a+1]-Time_Range[a])
print("时间间隔：")
print(Frequency)

#print(len(Time_Range))
#print(len(Frequency))
	
