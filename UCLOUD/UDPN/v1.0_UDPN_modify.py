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
Version: 1.0                                                                                      #
Release Date: 25/12/2023

使用须知：
1.请修改秘钥信息、通用信息、UDPN Info、共享带宽Info后再使用。
2.本脚本用于弹性调整UDPN和共享带宽，日志会分别存储为：udpn_modify.log、sharebandwidth_modify.log。
3.本脚本仅用于参考使用，不承担生产使用异常带来的风险。
'''

#修改为个人秘钥
#账号：1349826830@qq.com
Pubulic_Key = "2DVUfAN0VeWFBIV3OBjn9W9tWB5VqB7iOIN9OVuX7"
Private_Key = "FNoqMqrZqMY5mGpOFeudMzF8EfCtcvq838jVLBmOXavkFzkXlX3NjCE5Mf5OUmrwdf"

#通用信息
Project_ID = "org-en5c1p"
Region_A = "cn-gd"
Region_B = "cn-sh2"
Pace = [0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25]
Log_Path_UDPN = "/Users/fredshen/Downloads/uwork/API_test/udpn_modify.log"
Log_Path_ShareBandWidth = "/Users/fredshen/Downloads/uwork/API_test/sharebandwidth_modify.log"

#UDPN Info
UDPN_ID = "udpn-rv281e2zx6z"
Max_Limit_UDPN = 8000#带宽可调节上限值
Min_Limit_UDPN = 2#带宽可调节下限值（最小值2）

#ShareBnadwidth Info
Region_A_ShareBandwidthId = "xxx"
Region_B_ShareBandwidthId = "xxx"
Max_Limit_ShareBandwidth = 8000#带宽可调节上限值
Min_Limit_ShareBandwidth = 20#带宽可调节下限值（最小值20）

#---------请勿修改以下区域----------
client = Client({
	"region": Region_A,
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})

def describe_udpn():	
	try:
		resp1 = client.udpn().describe_udpn({
			"UDPNId": UDPN_ID
				
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp1)
		#a_Bandwidth = resp1.get('DataSet')[0].get('Bandwidth')	
	return(resp1)

def get_metric(Region):
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

def modify_udpn_bandwidth(New_Bandwidth):
	try:
		resp3 = client.udpn().modify_udpn_bandwidth({
			"UDPNId": UDPN_ID,
			"Bandwidth": New_Bandwidth
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp3)
	return(resp3)

def log(Log_DescribeUDPN,Log_GetMetric,Log_Judge,Log_ModifyUDPN,Log_Summary):
	#写日志
	try:
		# 打开文件并设置为追加模式（'a'表示追加）
		with open(Log_Path_UDPN, 'a') as file:
			# 将内容写入文件中
			file.write(Log_DescribeUDPN)
			file.write(Log_GetMetric)
			file.write(Log_Judge)
			file.write(Log_ModifyUDPN)
			file.write(Log_Summary+"\n")
			
		print("---------带宽调整成功---------")
		print("日志成功写入！")
	except Exception as e:
		print("发生错误：", str(e))
		
			


def modify():
	#获取带宽值
	Current_Bandwidth = describe_udpn().get('DataSet')[0].get('Bandwidth')

	
	#获取监控值
	Metric_A = get_metric(Region_A).get("DataSets")
	Metric_BandOut_A = Metric_A.get("BandOut")[-1].get("Value")
	Metric_BandOutMax_A = Metric_A.get("BandOutMax")[-1].get("Value")
	Metric_BandOutUsage_A = Metric_A.get("BandOutUsage")[-1].get("Value")
	Metric_BandOutMaxUsage_A = Metric_A.get("BandOutMaxUsage")[-1].get("Value")
	Metric_B = get_metric(Region_B).get("DataSets")
	Metric_BandOut_B = Metric_B.get("BandOut")[-1].get("Value")
	Metric_BandOutMax_B = Metric_B.get("BandOutMax")[-1].get("Value")
	Metric_BandOutUsage_B = Metric_B.get("BandOutUsage")[-1].get("Value")
	Metric_BandOutMaxUsage_B = Metric_B.get("BandOutMaxUsage")[-1].get("Value")
	if Metric_BandOutMaxUsage_A > Metric_BandOutMaxUsage_B:
		Metric_BandOutMaxUsage = Metric_BandOutMaxUsage_A
		Larger_Region = Region_A
		Metric_BandOutMaxUsage_Smaller = Metric_BandOutMaxUsage_B
		Smaller_Region = Region_A
	else:
		Metric_BandOutMaxUsage = Metric_BandOutMaxUsage_B
		Larger_Region = Region_B
		Smaller_Region = Region_A
		Metric_BandOutMaxUsage_Smaller = Metric_BandOutMaxUsage_A
		
	#判断
	if Metric_BandOutMaxUsage < 60:
		New_Bandwidth = int(Current_Bandwidth * Pace[0])#0.8
		if New_Bandwidth < Min_Limit_UDPN:
			New_Bandwidth = Min_Limit_UDPN
	elif Metric_BandOutMaxUsage >= 60 and Metric_BandOutMaxUsage < 70:
		New_Bandwidth = int(Current_Bandwidth * Pace[2])#0.9
		if New_Bandwidth < Min_Limit_UDPN:
			New_Bandwidth = Min_Limit_UDPN
	elif Metric_BandOutMaxUsage >= 70 and Metric_BandOutMaxUsage < 80:
		New_Bandwidth = int(Current_Bandwidth * Pace[3])#0.95
		if New_Bandwidth < Min_Limit_UDPN:
			New_Bandwidth = Min_Limit_UDPN
	elif Metric_BandOutMaxUsage >= 80 and Metric_BandOutMaxUsage < 90:
		New_Bandwidth = int(Current_Bandwidth * Pace[5])#1.05
		if New_Bandwidth > Max_Limit_UDPN:
			New_Bandwidth = Max_Limit_UDPN
	elif Metric_BandOutMaxUsage >= 90 and Metric_BandOutMaxUsage < 100:
		New_Bandwidth = int(Current_Bandwidth * Pace[6])#1.1
		if New_Bandwidth > Max_Limit_UDPN:
			New_Bandwidth = Max_Limit_UDPN
	elif Metric_BandOutMaxUsage >= 100 and Metric_BandOutMaxUsage < 110:
		New_Bandwidth = int(Current_Bandwidth * Pace[7])#1.15
		if New_Bandwidth > Max_Limit_UDPN:
			New_Bandwidth = Max_Limit_UDPN
	else:#即：>=110
		New_Bandwidth = int(Current_Bandwidth * Metric_BandOutMaxUsage * Pace[8] / 100)#1.2
		if New_Bandwidth > Max_Limit_UDPN:
			New_Bandwidth = Max_Limit_UDPN
				
	#调整带宽
	Modify_Record = modify_udpn_bandwidth(New_Bandwidth)
	
	#记录日志
	#例如：20231207 16:26 资源ID 区域a（高）带宽使用率 当前带宽值 调整带宽值 调整幅度 unxi时间戳 区域a 区域b
	Log_DescribeUDPN = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " "+UDPN_ID+" "+"当前带宽值："+str(Current_Bandwidth)
	Log_GetMetric = "，峰值使用率："+str(Metric_BandOutMaxUsage)+"%"
	Log_Judge = "，调整比例："+str(round(New_Bandwidth/Current_Bandwidth,2))
	Log_ModifyUDPN = "，新带宽值："+str(New_Bandwidth)
	Log_Summary = "，出口更大区域："+Larger_Region
	log(Log_DescribeUDPN,Log_GetMetric,Log_Judge,Log_ModifyUDPN,Log_Summary)
	print(Log_DescribeUDPN,Log_GetMetric,Log_Judge,Log_ModifyUDPN,Log_Summary)
	
#定时任务
def main():
	while True:
		modify()
		time.sleep(60)
if __name__ == '__main__':
	main()
	
	
	