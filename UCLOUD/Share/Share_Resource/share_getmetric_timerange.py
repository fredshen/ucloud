# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client
import time

#修改为个人秘钥
#账号：ibu-bot@ucloud.cn
Pubulic_Key = "4eZBe1JSbOaDrvqa0VoM1V5E3VYkiOTua"
Private_Key = "8BS9OGIisT58x76QWlK3zk8dZEmk702NM7BBuM5dZdGU"
Project_ID = "org-z50fdd"

ShareBandwidth_ID = "bwshare-rz4nwp4841k"
Region = "cn-gd"

#请勿随意修改以下信息
client = Client({
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})


def main():
	resp = client.invoke("GetMetric", {
		"Region": Region,
		"ProjectId": Project_ID,
		"ResourceType": "sharebandwidth",
		"ResourceId": ShareBandwidth_ID,
		"TimeRange": 3000,
		"MetricName.0": "NetworkOutUsage"
	})
	
	print("------------复制以下信息------------")
	
	
	Usage_Data = resp["DataSets"].get("NetworkOutUsage")
	
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


if __name__ == '__main__':
	main()
	
	