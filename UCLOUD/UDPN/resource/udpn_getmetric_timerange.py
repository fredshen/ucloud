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
#账号：1349826830@qq.com
Pubulic_Key = "2DVUfAN0VeWFBIV3OBjn9W9tWB5VqB7iOIN9OVuX7"
Private_Key = "FNoqMqrZqMY5mGpOFeudMzF8EfCtcvq838jVLBmOXavkFzkXlX3NjCE5Mf5OUmrwdf"

#
UDPN_ID = "udpn-rv281e2zx6z"
Project_ID = "org-en5c1p"
Region = "cn-gd"
Zone = "cn-gd-02"
#Log_Path = "/Users/fredshen/Downloads/uwork/API_test"

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
		#"Zone": Zone,
		"ProjectId": Project_ID,
		"ResourceType": "udpn",
		"ResourceId": UDPN_ID,
		"TimeRange": 3000,
		"MetricName.0": "BandOutMaxUsage"
	})
	
	print("------------复制以下信息------------")
	
	
	Usage_Data = resp["DataSets"].get("BandOutMaxUsage")
	
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
	
	