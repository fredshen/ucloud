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
Version: 1.2
Release Date: 28/12/2023

使用须知：
1.请修改秘钥信息、通用信息、UDPN Info、ShareBnadwidth Info后再使用。
2.本脚本用于弹性调整UDPN和共享带宽，日志会分别存储为：udpn_modify.log、sharebandwidth_modify.log。
3.本脚本仅用于参考使用，不承担生产使用异常带来的风险。


Release Note:
Version: 1.2
1.修改GetMetric获取的监控类型，只获取峰值带宽使用率
'''

#修改为个人秘钥
#账号：ibu-bot@ucloud.cn
Pubulic_Key = "4eZBe1JSbOaDrvqa0VoM1V5E3VYkiOTua"
Private_Key = "8BS9OGIisT58x76QWlK3zk8dZEmk702NM7BBuM5dZdGU"
Project_ID = "org-z50fdd"

#通用信息
Pace = [0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25]
UDPN_Log_Path = "/Users/fredshen/Downloads/uwork/API_test/udpn_modify.log"
ShareBandwidth_Log_Path = "/Users/fredshen/Downloads/uwork/API_test/sharebandwidth_modify.log"

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

#1.1 获取UDPN带宽值
def describe_udpn():	
	try:
		resp1 = client.udpn().describe_udpn({
			"UDPNId": UDPN_ID,
			"Region": Region_A
				
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp1)
		#a_Bandwidth = resp1.get('DataSet')[0].get('Bandwidth')	
	return(resp1)

#1.2 获取共享带宽值
def describe_share_bandwidth(Region,ShareBandwidthId):
	try:
		resp2 = client.unet().describe_share_bandwidth({
			"Region": Region,
			"ShareBandwidthIds": [
				ShareBandwidthId
			]
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp2)
	return(resp2)

#2 获取UDPN&共享带宽监控值
def get_metric(Region,ResourceType,ShareBandwidthId,MetricName0,MetricName1):
	try:
		resp3 = client.invoke("GetMetric", {
			"Region": Region,
			"ProjectId": Project_ID,
			"ResourceType": ResourceType,
			"ResourceId": ShareBandwidthId,
			"TimeRange": 200,
			"MetricName.0": MetricName0,
			"MetricName.1": MetricName1
	})
	except exc.RetCodeException as e:
		resp3 = e.json()
	return(resp3)

#3 判断
def judge(Judge_Metric_Data,Current_Bandwidth,Resource_Type):
	#设置上/下限
	if Resource_Type == "UDPN":
		Max_Limit = Max_Limit_UDPN
		Min_Limit = Min_Limit_UDPN
	elif Resource_Type == "ShareBandwidth":
		Max_Limit = Max_Limit_ShareBandwidth
		Min_Limit = Min_Limit_ShareBandwidth
	#Judge
	if Judge_Metric_Data < 60:
		New_Bandwidth = int(Current_Bandwidth * Pace[0])#0.8
		if New_Bandwidth == Current_Bandwidth:
			New_Bandwidth = Current_Bandwidth +1
		if New_Bandwidth < Min_Limit:
			New_Bandwidth = Min_Limit
	elif Judge_Metric_Data >= 60 and Judge_Metric_Data < 70:
		New_Bandwidth = int(Current_Bandwidth * Pace[2])#0.9
		if New_Bandwidth == Current_Bandwidth:
			New_Bandwidth = Current_Bandwidth +1
		if New_Bandwidth < Min_Limit:
			New_Bandwidth = Min_Limit
	elif Judge_Metric_Data >= 70 and Judge_Metric_Data < 80:
		New_Bandwidth = int(Current_Bandwidth * Pace[3])#0.95
		if New_Bandwidth == Current_Bandwidth:
			New_Bandwidth = Current_Bandwidth +1
		if New_Bandwidth < Min_Limit:
			New_Bandwidth = Min_Limit
	elif Judge_Metric_Data >= 80 and Judge_Metric_Data < 90:
		New_Bandwidth = int(Current_Bandwidth * Pace[5])#1.05
		if New_Bandwidth == Current_Bandwidth:
			New_Bandwidth = Current_Bandwidth +1
		if New_Bandwidth > Max_Limit:
			New_Bandwidth = Max_Limit
	elif Judge_Metric_Data >= 90 and Judge_Metric_Data < 100:
		New_Bandwidth = int(Current_Bandwidth * Pace[6])#1.1
		if New_Bandwidth == Current_Bandwidth:
			New_Bandwidth = Current_Bandwidth +1
		if New_Bandwidth > Max_Limit:
			New_Bandwidth = Max_Limit
	elif Judge_Metric_Data >= 100 and Judge_Metric_Data < 110:
		New_Bandwidth = int(Current_Bandwidth * Pace[7])#1.15
		if New_Bandwidth == Current_Bandwidth:
			New_Bandwidth = Current_Bandwidth +1
		if New_Bandwidth > Max_Limit:
			New_Bandwidth = Max_Limit
	else:#即：>=110
		New_Bandwidth = int(Judge_Metric_Data / 100 * Current_Bandwidth * Pace[8])#1.2
		if New_Bandwidth == Current_Bandwidth:
			New_Bandwidth = Current_Bandwidth +1
		if New_Bandwidth > Max_Limit:
			New_Bandwidth = Max_Limit
	return New_Bandwidth

#4.1 修改UDPN带宽值
def modify_udpn_bandwidth(New_Bandwidth_UDPN):
	try:
		resp4 = client.udpn().modify_udpn_bandwidth({
			"UDPNId": UDPN_ID,
			"region": Region_A,
			"Bandwidth": New_Bandwidth_UDPN
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp4)
	return(resp4)
#4.2 修改共享带宽值
def resize_share_bandwidth(Region,New_Bandwidth_Share,ShareBandwidthId):
	try:
		resp5 = client.unet().resize_share_bandwidth({
			"Region": Region,
			"ShareBandwidth": New_Bandwidth_Share,
			"ShareBandwidthId": ShareBandwidthId
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp5)

#5 写日志
def log(Log_Path,Log_Describe,Log_GetMetric,Log_Judge,Log_Modify,Log_Summary):
	#写日志
	try:
		# 打开文件并设置为追加模式（'a'表示追加）
		with open(Log_Path, 'a') as file:
			# 将内容写入文件中
			file.write(Log_Describe)
			file.write(Log_GetMetric)
			file.write(Log_Judge)
			file.write(Log_Modify)
			file.write(Log_Summary+"\n")
			
		print("---------带宽调整成功---------日志成功写入！")
	except Exception as e:
		print("发生错误：", str(e))
		

def modify():
	#二、1 获取UDPN&共享带宽带宽值
	UDPN_Current_Bandwidth = describe_udpn().get('DataSet')[0].get('Bandwidth')
	ShareBandWidth_Current_Bandwidth_Region_A = describe_share_bandwidth(Region_A,Region_A_ShareBandwidthId).get("DataSet")[0].get("ShareBandwidth")
	ShareBandWidth_Current_Bandwidth_Region_B = describe_share_bandwidth(Region_B,Region_B_ShareBandwidthId).get("DataSet")[0].get("ShareBandwidth")
	
	#二、2 获取UDPN&共享带宽监控值
	UDPN_Metric_A = get_metric(Region_A,"udpn",UDPN_ID,"BandOutUsage","BandOutMaxUsage").get("DataSets")
	UDPN_Metric_B = get_metric(Region_B,"udpn",UDPN_ID,"BandOutUsage","BandOutMaxUsage").get("DataSets")
	ShareBandwidth_Metric_A = get_metric(Region_A,"sharebandwidth",Region_A_ShareBandwidthId,"NetworkInUsage","NetworkOutUsage").get("DataSets")
	ShareBandwidth_Metric_B = get_metric(Region_B,"sharebandwidth",Region_B_ShareBandwidthId,"NetworkInUsage","NetworkOutUsage").get("DataSets")
	
	Metric_Data = {}
	for i in ["A","B"]:
		for a in ["BandOutUsage","BandOutMaxUsage"]:
			UDPN_Metric_Name = f"UDPN_{a}" f"_{i}"
			UDPN_Metric_Value = eval(f"UDPN_Metric_{i}").get(a)[-1].get("Value")
			Metric_Data[UDPN_Metric_Name] = UDPN_Metric_Value
			
		for b in ["NetworkInUsage","NetworkOutUsage"]:
			ShareBandwidth_Metric_Name = f"ShareBandwidth_{b}" f"_{i}"
			ShareBandwidth_Metric_Value = eval(f"ShareBandwidth_Metric_{i}").get(b)[-1].get("Value")
			Metric_Data[ShareBandwidth_Metric_Name] = ShareBandwidth_Metric_Value
	
	#二、3 Judge
	if Metric_Data["UDPN_BandOutMaxUsage_A"] > Metric_Data["UDPN_BandOutMaxUsage_B"]:
		UDPN_Metric_Data = Metric_Data["UDPN_BandOutMaxUsage_A"]
		UDPN_Larger = Region_A
	else:
		UDPN_Metric_Data = Metric_Data["UDPN_BandOutMaxUsage_B"]
		UDPN_Larger = Region_B
	
	if Metric_Data["ShareBandwidth_NetworkInUsage_A"] > Metric_Data["ShareBandwidth_NetworkOutUsage_A"]:
		ShareBandwidth_Metric_Data_A = Metric_Data["ShareBandwidth_NetworkInUsage_A"]
		ShareBandwidth_Larger_A = "入向"
	else:
		ShareBandwidth_Metric_Data_A = Metric_Data["ShareBandwidth_NetworkOutUsage_A"]
		ShareBandwidth_Larger_A = "出向"
		
	if Metric_Data["ShareBandwidth_NetworkInUsage_B"] > Metric_Data["ShareBandwidth_NetworkOutUsage_B"]:
		ShareBandwidth_Metric_Data_B = Metric_Data["ShareBandwidth_NetworkInUsage_B"]
		ShareBandwidth_Larger_B = "入向"
	else:
		ShareBandwidth_Metric_Data_B = Metric_Data["ShareBandwidth_NetworkOutUsage_B"]
		ShareBandwidth_Larger_B = "出向"
		
	UDPN_New_Bandwidth = judge(UDPN_Metric_Data,UDPN_Current_Bandwidth,"UDPN")
	ShareBandWidth_New_Bandwidth_Region_A = judge(ShareBandwidth_Metric_Data_A,ShareBandWidth_Current_Bandwidth_Region_A,"ShareBandwidth")
	ShareBandWidth_New_Bandwidth_Region_B = judge(ShareBandwidth_Metric_Data_B,ShareBandWidth_Current_Bandwidth_Region_B,"ShareBandwidth")
	
	
	#调整带宽
	UDPN_Modify_Record = modify_udpn_bandwidth(UDPN_New_Bandwidth)
	ShareBandWidth_Modify_Record_A = resize_share_bandwidth(Region_A, ShareBandWidth_New_Bandwidth_Region_A, Region_A_ShareBandwidthId)
	ShareBandWidth_Modify_Record_B = resize_share_bandwidth(Region_B, ShareBandWidth_New_Bandwidth_Region_B, Region_B_ShareBandwidthId)
	
	#记录UDPN日志
	UDPN_Log_Describe = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" "+UDPN_ID + " "+Region_A +"至"+Region_B+" "+"当前带宽值："+str(UDPN_Current_Bandwidth)
	UDPN_Log_GetMetric = "，峰值使用率："+str(UDPN_Metric_Data)+"%"
	UDPN_Log_Judge = "，调整比例："+str(round(UDPN_New_Bandwidth/UDPN_Current_Bandwidth,2))
	UDPN_Log_Modify = "，新带宽值："+str(UDPN_New_Bandwidth)
	UDPN_Log_Summary = "，出口更大区域："+UDPN_Larger
	log(UDPN_Log_Path,UDPN_Log_Describe,UDPN_Log_GetMetric,UDPN_Log_Judge,UDPN_Log_Modify,UDPN_Log_Summary)
	print(UDPN_Log_Describe,UDPN_Log_GetMetric,UDPN_Log_Judge,UDPN_Log_Modify,UDPN_Log_Summary)
	
	#记录共享带宽_A日志
	ShareBandWidth_Log_Describe_A = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" "+Region_A_ShareBandwidthId + " "+Region_A +" "+"当前带宽值："+str(ShareBandWidth_Current_Bandwidth_Region_A)
	ShareBandWidth_Log_GetMetric_A = "，带宽使用率："+str(ShareBandwidth_Metric_Data_A)+"%"
	ShareBandWidth_Log_Judge_A = "，调整比例："+str(round(ShareBandWidth_New_Bandwidth_Region_A/ShareBandWidth_Current_Bandwidth_Region_A,2))
	ShareBandWidth_Log_Modify_A = "，新带宽值："+str(ShareBandWidth_New_Bandwidth_Region_A)
	ShareBandWidth_Log_Summary_A = "，出口更大区域："+ShareBandwidth_Larger_A
	
	log(ShareBandwidth_Log_Path,ShareBandWidth_Log_Describe_A,ShareBandWidth_Log_GetMetric_A,ShareBandWidth_Log_Judge_A,ShareBandWidth_Log_Modify_A,ShareBandWidth_Log_Summary_A)
	print(ShareBandWidth_Log_Describe_A,ShareBandWidth_Log_GetMetric_A,ShareBandWidth_Log_Judge_A,ShareBandWidth_Log_Modify_A,ShareBandWidth_Log_Summary_A)
	
	#记录共享带宽_B日志
	ShareBandWidth_Log_Describe_B = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" "+Region_B_ShareBandwidthId + " "+Region_B +" "+"当前带宽值："+str(ShareBandWidth_Current_Bandwidth_Region_B)
	ShareBandWidth_Log_GetMetric_B = "，带宽使用率："+str(ShareBandwidth_Metric_Data_B)+"%"
	ShareBandWidth_Log_Judge_B = "，调整比例："+str(round(ShareBandWidth_New_Bandwidth_Region_B/ShareBandWidth_Current_Bandwidth_Region_B,2))
	ShareBandWidth_Log_Modify_B = "，新带宽值："+str(ShareBandWidth_New_Bandwidth_Region_B)
	ShareBandWidth_Log_Summary_B = "，出口更大区域："+ShareBandwidth_Larger_B
	log(ShareBandwidth_Log_Path,ShareBandWidth_Log_Describe_B,ShareBandWidth_Log_GetMetric_B,ShareBandWidth_Log_Judge_B,ShareBandWidth_Log_Modify_B,ShareBandWidth_Log_Summary_B)
	print(ShareBandWidth_Log_Describe_B,ShareBandWidth_Log_GetMetric_B,ShareBandWidth_Log_Judge_B,ShareBandWidth_Log_Modify_B,ShareBandWidth_Log_Summary_B)
	
	
	
#定时任务
def main():
	while True:
		modify()
		time.sleep(10)
if __name__ == '__main__':
	main()