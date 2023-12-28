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

'''
Author: F.Shen（fred.shen@ucloud.cn）
Version: 1.1
Release Date: 25/12/2023

使用须知：
1.请修改秘钥信息、通用信息、UDPN Info、ShareBnadwidth Info后再使用。
2.本脚本用于弹性调整UDPN和共享带宽，日志会分别存储为：udpn_modify.log、sharebandwidth_modify.log。
3.本脚本仅用于参考使用，不承担生产使用异常带来的风险。
'''

#修改为个人秘钥
#账号：ibu-bot@ucloud.cn
Pubulic_Key = "4eZBe1JSbOaDrvqa0VoM1V5E3VYkiOTua"
Private_Key = "8BS9OGIisT58x76QWlK3zk8dZEmk702NM7BBuM5dZdGU"
Project_ID = "org-z50fdd"

#通用信息
Pace = [0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25]
Log_Path_UDPN = "/Users/fredshen/Downloads/uwork/API_test/udpn_modify.log"
Log_Path_ShareBandWidth = "/Users/fredshen/Downloads/uwork/API_test/sharebandwidth_modify.log"

#ShareBnadwidth Info
Region_A = "cn-sh2"
Region_A_ShareBandwidthId = "bwshare-rz4o9mfbqz2"#与Region_A对应
Region_B = "cn-gd"
Region_B_ShareBandwidthId = "bwshare-rz4nwp4841k"#与Region_B对应
Max_Limit_ShareBandwidth = 8000#带宽可调节上限值
Min_Limit_ShareBandwidth = 20#带宽可调节下限值（最小值20）

#UDPN Info
UDPN_ID = "udpn-rz4qvyv99he"
Max_Limit_UDPN = 8000#带宽可调节上限值
Min_Limit_UDPN = 2#带宽可调节下限值（最小值2）



#---------请勿修改以下区域----------
client = Client({
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})

'''
def get_metric_udpn(Region):
	try:
		resp2 = client.invoke("GetMetric", {
			"Region": Region,
			"ProjectId": Project_ID,
			"ResourceType": "udpn",
			"ResourceId": UDPN_ID,
			"TimeRange": 200,
			"MetricName.0": "BandOut",
			"MetricName.1": "BandOutMax",
			"MetricName.2": "BandOutUsage",
			"MetricName.3": "BandOutMaxUsage"
	})
	except exc.RetCodeException as e:
		resp2 = e.json()
	return(resp2)
'''

#获取监控值
def get_metric(Region,ResourceType,ShareBandwidthId,MetricName0,MetricName1,MetricName2,MetricName3):
	try:
		resp5 = client.invoke("GetMetric", {
			"Region": Region,
			"ProjectId": Project_ID,
			"ResourceType": ResourceType,
			"ResourceId": ShareBandwidthId,
			"TimeRange": 200,
			"MetricName.0": MetricName0,
			"MetricName.1": MetricName1,
			"MetricName.2": MetricName2,
			"MetricName.3": MetricName3
	})
	except exc.RetCodeException as e:
		resp5 = e.json()
	return(resp5)



#获取监控值
Metric_UDPN_A = get_metric(Region_A,"udpn",UDPN_ID,"BandOut","BandOutMax","BandOutUsage","BandOutMaxUsage").get("DataSets")
Metric_BandOut_UDPN_A = Metric_UDPN_A.get("BandOut")[-1].get("Value")
Metric_BandOutMax_UDPN_A = Metric_UDPN_A.get("BandOutMax")[-1].get("Value")
Metric_BandOutUsage_UDPN_A = Metric_UDPN_A.get("BandOutUsage")[-1].get("Value")
Metric_BandOutMaxUsage_UDPN_A = Metric_UDPN_A.get("BandOutMaxUsage")[-1].get("Value")
Metric_UDPN_B = get_metric(Region_B,"udpn",UDPN_ID,"BandOut","BandOutMax","BandOutUsage","BandOutMaxUsage").get("DataSets")
Metric_BandOut_UDPN_B = Metric_UDPN_B.get("BandOut")[-1].get("Value")
Metric_BandOutMax_UDPN_B = Metric_UDPN_B.get("BandOutMax")[-1].get("Value")
Metric_BandOutUsage_UDPN_B = Metric_UDPN_B.get("BandOutUsage")[-1].get("Value")
Metric_BandOutMaxUsage_UDPN_B = Metric_UDPN_B.get("BandOutMaxUsage")[-1].get("Value")


print("-----------------")
print(Metric_UDPN_A)
print(Metric_UDPN_B)

'''
#获取监控值
Metric_Share_A = getmetric_share(Region_A, Region_A_ShareBandwidthId).get("DataSets")
Metric_Share_A_BandIn = Metric_Share_A.get("BandIn")[-1].get("Value")
Metric_Share_A_BandOut = Metric_Share_A.get("BandOut")[-1].get("Value")
Metric_Share_A_NetworkInUsage = Metric_Share_A.get("NetworkInUsage")[-1].get("Value")
Metric_Share_A_NetworkOutUsage = Metric_Share_A.get("NetworkOutUsage")[-1].get("Value")

Metric_Share_B = getmetric_share(Region_B, Region_B_ShareBandwidthId).get("DataSets")
Metric_Share_B_BandIn = Metric_Share_B.get("BandIn")[-1].get("Value")
Metric_Share_B_BandOut = Metric_Share_B.get("BandOut")[-1].get("Value")
Metric_Share_B_NetworkInUsage = Metric_Share_B.get("NetworkInUsage")[-1].get("Value")
Metric_Share_B_NetworkOutUsage = Metric_Share_B.get("NetworkOutUsage")[-1].get("Value")
'''