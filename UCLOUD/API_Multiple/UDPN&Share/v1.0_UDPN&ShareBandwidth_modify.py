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

#UDPN Info
UDPN_ID = "udpn-rz4qvyv99he"
Max_Limit_UDPN = 8000#带宽可调节上限值
Min_Limit_UDPN = 2#带宽可调节下限值（最小值2）

#ShareBnadwidth Info
Region_A = "cn-sh2"
Region_A_ShareBandwidthId = "bwshare-rz4o9mfbqz2"#与Region_A对应
Region_B = "cn-gd"
Region_B_ShareBandwidthId = "bwshare-rz4nwp4841k"#与Region_B对应
Max_Limit_ShareBandwidth = 8000#带宽可调节上限值
Min_Limit_ShareBandwidth = 20#带宽可调节下限值（最小值20）

#---------请勿修改以下区域----------
client = Client({
	#"region": Region_A,
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})

#UDPN
def describe_udpn():	
	try:
		resp1 = client.udpn().describe_udpn({
			"UDPNId": UDPN_ID,
			"region": Region_A
				
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp1)
		#a_Bandwidth = resp1.get('DataSet')[0].get('Bandwidth')	
	return(resp1)

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

def modify_udpn_bandwidth(New_Bandwidth_UDPN):
	try:
		resp3 = client.udpn().modify_udpn_bandwidth({
			"UDPNId": UDPN_ID,
			"region": Region_A,
			"Bandwidth": New_Bandwidth_UDPN
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp3)
	return(resp3)

def log_UDPN(Log_DescribeUDPN,Log_GetMetric_UDPN,Log_Judge_UDPN,Log_ModifyUDPN,Log_Summary_UDPN):
	#写日志
	try:
		# 打开文件并设置为追加模式（'a'表示追加）
		with open(Log_Path_UDPN, 'a') as file:
			# 将内容写入文件中
			file.write(Log_DescribeUDPN)
			file.write(Log_GetMetric_UDPN)
			file.write(Log_Judge_UDPN)
			file.write(Log_ModifyUDPN)
			file.write(Log_Summary_UDPN+"\n")
			
		print("---------UDPN带宽调整成功---------")
		print("UDPN日志成功写入！")
	except Exception as e:
		print("发生错误：", str(e))

#共享带宽
#获取带宽值
def describe_share_bandwidth(Region,ShareBandwidthId):
	try:
		resp4 = client.unet().describe_share_bandwidth({
			"Region": Region,
			"ShareBandwidthIds": [
				ShareBandwidthId
			]
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp4)
	return(resp4)

#获取监控值
def getmetric_share(Region,ShareBandwidthId):
	try:
		resp5 = client.invoke("GetMetric", {
			"Region": Region,
			#"Zone": "cn-sh2-01",
			"ProjectId": Project_ID,
			"ResourceType": "sharebandwidth",
			"ResourceId": ShareBandwidthId,
			"TimeRange": 200,
			"MetricName.0": "BandIn",
			"MetricName.1": "BandOut",
			"MetricName.2": "NetworkInUsage",
			"MetricName.3": "NetworkOutUsage"
	})
	except exc.RetCodeException as e:
		resp5 = e.json()
	return(resp5)

#判断



#调整带宽
def resize_share_bandwidth(Region,New_Bandwidth_Share,ShareBandwidthId):
	try:
		resp6 = client.unet().resize_share_bandwidth({
			"Region": Region,
			"ShareBandwidth": New_Bandwidth_Share,
			"ShareBandwidthId": ShareBandwidthId
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp6)


#写共享带宽日志
def log_ShareBandwidth(Log_DescribeShare,Log_GetMetric_share,Log_Judge_share,Log_Modifyshare,Log_Summary_share):
	#写日志
	try:
		# 打开文件并设置为追加模式（'a'表示追加）
		with open(Log_Path_ShareBandWidth, 'a') as file:
			# 将内容写入文件中
			file.write(Log_DescribeShare)
			file.write(Log_GetMetric_share)
			file.write(Log_Judge_share)
			file.write(Log_Modifyshare)
			file.write(Log_Summary_share+"\n")
			
		print("---------共享带宽调整成功---------")
		print("共享带宽日志成功写入！")
	except Exception as e:
		print("发生错误：", str(e))









def modify_udpn():
	#获取带宽值
	Current_Bandwidth_UDPN = describe_udpn().get('DataSet')[0].get('Bandwidth')

	
	#获取监控值
	Metric_UDPN_A = get_metric_udpn(Region_A).get("DataSets")
	Metric_BandOut_UDPN_A = Metric_UDPN_A.get("BandOut")[-1].get("Value")
	Metric_BandOutMax_UDPN_A = Metric_UDPN_A.get("BandOutMax")[-1].get("Value")
	Metric_BandOutUsage_UDPN_A = Metric_UDPN_A.get("BandOutUsage")[-1].get("Value")
	Metric_BandOutMaxUsage_UDPN_A = Metric_UDPN_A.get("BandOutMaxUsage")[-1].get("Value")
	Metric_B = get_metric_udpn(Region_B).get("DataSets")
	Metric_BandOut_UDPN_B = Metric_B.get("BandOut")[-1].get("Value")
	Metric_BandOutMax_UDPN_B = Metric_B.get("BandOutMax")[-1].get("Value")
	Metric_BandOutUsage_UDPN_B = Metric_B.get("BandOutUsage")[-1].get("Value")
	Metric_BandOutMaxUsage_UDPN_B = Metric_B.get("BandOutMaxUsage")[-1].get("Value")
	if Metric_BandOutMaxUsage_UDPN_A > Metric_BandOutMaxUsage_UDPN_B:
		Metric_BandOutMaxUsage_UDPN = Metric_BandOutMaxUsage_UDPN_A
		Larger_Region_UDPN = Region_A
		Metric_BandOutMaxUsage_UDPN_Smaller = Metric_BandOutMaxUsage_UDPN_B
		Smaller_Region_UDPN = Region_A
	else:
		Metric_BandOutMaxUsage_UDPN = Metric_BandOutMaxUsage_UDPN_B
		Larger_Region_UDPN = Region_B
		Smaller_Region_UDPN = Region_A
		Metric_BandOutMaxUsage_UDPN_Smaller = Metric_BandOutMaxUsage_UDPN_A
		
	#判断
	if Metric_BandOutMaxUsage_UDPN < 60:
		New_Bandwidth_UDPN = int(Current_Bandwidth_UDPN * Pace[0])#0.8
		if New_Bandwidth_UDPN < Min_Limit_UDPN:
			New_Bandwidth_UDPN = Min_Limit_UDPN
	elif Metric_BandOutMaxUsage_UDPN >= 60 and Metric_BandOutMaxUsage_UDPN < 70:
		New_Bandwidth_UDPN = int(Current_Bandwidth_UDPN * Pace[2])#0.9
		if New_Bandwidth_UDPN < Min_Limit_UDPN:
			New_Bandwidth_UDPN = Min_Limit_UDPN
	elif Metric_BandOutMaxUsage_UDPN >= 70 and Metric_BandOutMaxUsage_UDPN < 80:
		New_Bandwidth_UDPN = int(Current_Bandwidth_UDPN * Pace[3])#0.95
		if New_Bandwidth_UDPN < Min_Limit_UDPN:
			New_Bandwidth_UDPN = Min_Limit_UDPN
	elif Metric_BandOutMaxUsage_UDPN >= 80 and Metric_BandOutMaxUsage_UDPN < 90:
		New_Bandwidth_UDPN = int(Current_Bandwidth_UDPN * Pace[5])#1.05
		if New_Bandwidth_UDPN > Max_Limit_UDPN:
			New_Bandwidth_UDPN = Max_Limit_UDPN
	elif Metric_BandOutMaxUsage_UDPN >= 90 and Metric_BandOutMaxUsage_UDPN < 100:
		New_Bandwidth_UDPN = int(Current_Bandwidth_UDPN * Pace[6])#1.1
		if New_Bandwidth_UDPN > Max_Limit_UDPN:
			New_Bandwidth_UDPN = Max_Limit_UDPN
	elif Metric_BandOutMaxUsage_UDPN >= 100 and Metric_BandOutMaxUsage_UDPN < 110:
		New_Bandwidth_UDPN = int(Current_Bandwidth_UDPN * Pace[7])#1.15
		if New_Bandwidth_UDPN > Max_Limit_UDPN:
			New_Bandwidth_UDPN = Max_Limit_UDPN
	else:#即：>=110
		New_Bandwidth_UDPN = int(Current_Bandwidth_UDPN * Metric_BandOutMaxUsage_UDPN * Pace[8] / 100)#1.2
		if New_Bandwidth_UDPN > Max_Limit_UDPN:
			New_Bandwidth_UDPN = Max_Limit_UDPN
				
	#调整带宽
	Modify_Record_UDPN = modify_udpn_bandwidth(New_Bandwidth_UDPN)
	
	#记录日志
	#例如：20231207 16:26 资源ID 区域a（高）带宽使用率 当前带宽值 调整带宽值 调整幅度 unxi时间戳 区域a 区域b
	Log_DescribeUDPN = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" "+UDPN_ID + " "+Region_A +"至"+Region_B+" "+"当前带宽值："+str(Current_Bandwidth_UDPN)
	Log_GetMetric_UDPN = "，峰值使用率："+str(Metric_BandOutMaxUsage_UDPN)+"%"
	Log_Judge_UDPN = "，调整比例："+str(round(New_Bandwidth_UDPN/Current_Bandwidth_UDPN,2))
	Log_ModifyUDPN = "，新带宽值："+str(New_Bandwidth_UDPN)
	Log_Summary_UDPN = "，出口更大区域："+Larger_Region_UDPN
	log_UDPN(Log_DescribeUDPN,Log_GetMetric_UDPN,Log_Judge_UDPN,Log_ModifyUDPN,Log_Summary_UDPN)
	print(Log_DescribeUDPN,Log_GetMetric_UDPN,Log_Judge_UDPN,Log_ModifyUDPN,Log_Summary_UDPN)
	
	#def modify_sharebandwidth():
	#print("")
	

def modify_sharebandwidth():
	#获取带宽值
	Current_Bandwidth_Share_Region_A = describe_share_bandwidth(Region_A,Region_A_ShareBandwidthId).get("DataSet")[0].get("ShareBandwidth")
	Current_Bandwidth_Share_Region_B = describe_share_bandwidth(Region_B,Region_B_ShareBandwidthId).get("DataSet")[0].get("ShareBandwidth")
	
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
	
	if Metric_Share_A_NetworkInUsage > Metric_Share_A_NetworkOutUsage:
		Metric_Share_A = Metric_Share_A_NetworkInUsage
		Larger_share_A = "入向"
	else:
		Metric_Share_A = Metric_Share_A_NetworkOutUsage
		Larger_share_A = "出向"
		
	if Metric_Share_B_NetworkInUsage > Metric_Share_B_NetworkOutUsage:
		Metric_Share_B = Metric_Share_B_NetworkInUsage
		Larger_share_B = "入向"
	else:
		Metric_Share_B = Metric_Share_B_NetworkOutUsage
		Larger_share_B = "出向"
	

	
	#判断A
	if Metric_Share_A < 60:
		New_Bandwidth_Share_Region_A = int(Current_Bandwidth_Share_Region_A * Pace[0])#0.8
		if New_Bandwidth_Share_Region_A < Min_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_A = Min_Limit_ShareBandwidth
	elif Metric_Share_A >= 60 and Metric_Share_A < 70:
		New_Bandwidth_Share_Region_A = int(Current_Bandwidth_Share_Region_A * Pace[2])#0.9
		if New_Bandwidth_Share_Region_A < Min_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_A = Min_Limit_ShareBandwidth
	elif Metric_Share_A >= 70 and Metric_Share_A < 80:
		New_Bandwidth_Share_Region_A = int(Current_Bandwidth_Share_Region_A * Pace[3])#0.95
		if New_Bandwidth_Share_Region_A < Min_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_A = Min_Limit_ShareBandwidth
	elif Metric_Share_A >= 80 and Metric_Share_A < 90:
		New_Bandwidth_Share_Region_A = int(Current_Bandwidth_Share_Region_A * Pace[5])#1.05
		if New_Bandwidth_Share_Region_A > Max_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_A = Max_Limit_ShareBandwidth
	elif Metric_Share_A >= 90 and Metric_Share_A < 100:
		New_Bandwidth_Share_Region_A = int(Current_Bandwidth_Share_Region_A * Pace[6])#1.1
		if New_Bandwidth_Share_Region_A > Max_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_A = Max_Limit_ShareBandwidth
	elif Metric_Share_A >= 100 and Metric_Share_A < 110:
		New_Bandwidth_Share_Region_A = int(Current_Bandwidth_Share_Region_A * Pace[7])#1.15
		if New_Bandwidth_Share_Region_A > Max_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_A = Max_Limit_ShareBandwidth
	else:#即：>=110
		New_Bandwidth_Share_Region_A = int(Current_Bandwidth_Share_Region_A * Metric_Share_A * Pace[8] / 100)#1.2
		if New_Bandwidth_Share_Region_A > Max_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_A = Max_Limit_ShareBandwidth
	#判断B
	if Metric_Share_B < 60:
		New_Bandwidth_Share_Region_B = int(Current_Bandwidth_Share_Region_B * Pace[0])#0.8
		if New_Bandwidth_Share_Region_B < Min_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_B = Min_Limit_ShareBandwidth
	elif Metric_Share_B >= 60 and Metric_Share_B < 70:
		New_Bandwidth_Share_Region_B = int(Current_Bandwidth_Share_Region_B * Pace[2])#0.9
		if New_Bandwidth_Share_Region_B < Min_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_B = Min_Limit_ShareBandwidth
	elif Metric_Share_B >= 70 and Metric_Share_B < 80:
		New_Bandwidth_Share_Region_B = int(Current_Bandwidth_Share_Region_B * Pace[3])#0.95
		if New_Bandwidth_Share_Region_B < Min_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_B = Min_Limit_ShareBandwidth
	elif Metric_Share_B >= 80 and Metric_Share_B < 90:
		New_Bandwidth_Share_Region_B = int(Current_Bandwidth_Share_Region_B * Pace[5])#1.05
		if New_Bandwidth_Share_Region_B > Max_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_B = Max_Limit_ShareBandwidth
	elif Metric_Share_B >= 90 and Metric_Share_B < 100:
		New_Bandwidth_Share_Region_B = int(Current_Bandwidth_Share_Region_B * Pace[6])#1.1
		if New_Bandwidth_Share_Region_B > Max_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_B = Max_Limit_ShareBandwidth
	elif Metric_Share_B >= 100 and Metric_Share_B < 110:
		New_Bandwidth_Share_Region_B = int(Current_Bandwidth_Share_Region_B * Pace[7])#1.15
		if New_Bandwidth_Share_Region_B > Max_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_B = Max_Limit_ShareBandwidth
	else:#即：>=110
		New_Bandwidth_Share_Region_B = int(Current_Bandwidth_Share_Region_B * Metric_Share_B * Pace[8] / 100)#1.2
		if New_Bandwidth_Share_Region_B > Max_Limit_ShareBandwidth:
			New_Bandwidth_Share_Region_B = Max_Limit_ShareBandwidth




	#调整带宽
	Modify_Record_Share_Region_A = resize_share_bandwidth(Region_A,New_Bandwidth_Share_Region_A,Region_A_ShareBandwidthId)
	Modify_Record_Share_Region_B = resize_share_bandwidth(Region_B,New_Bandwidth_Share_Region_B,Region_B_ShareBandwidthId)

	#记录共享带宽日志
	Log_DescribeShare_A = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " "+ Region_A_ShareBandwidthId + " "+ Region_A +" "+"当前带宽值："+str(Current_Bandwidth_Share_Region_A)
	Log_GetMetric_share_A = "，带宽使用率："+str(Metric_Share_A)+"%"
	Log_Judge_share_A = "，调整比例："+str(round(New_Bandwidth_Share_Region_A/Current_Bandwidth_Share_Region_A,2))
	Log_Modifyshare_A = "，新带宽值："+str(New_Bandwidth_Share_Region_A)
	Log_Summary_share_A = "，带宽更大为：："+ Larger_share_A
	log_ShareBandwidth(Log_DescribeShare_A,Log_GetMetric_share_A,Log_Judge_share_A,Log_Modifyshare_A,Log_Summary_share_A)
	print(Log_DescribeShare_A,Log_GetMetric_share_A,Log_Judge_share_A,Log_Modifyshare_A,Log_Summary_share_A)
	
	#记录共享带宽日志
	Log_DescribeShare_B = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " "+ Region_B_ShareBandwidthId + " "+ Region_B+" "+"当前带宽值："+str(Current_Bandwidth_Share_Region_B)
	Log_GetMetric_share_B = "，带宽使用率："+str(Metric_Share_B)+"%"
	Log_Judge_share_B = "，调整比例："+str(round(New_Bandwidth_Share_Region_B/Current_Bandwidth_Share_Region_B,2))
	Log_Modifyshare_B = "，新带宽值："+str(New_Bandwidth_Share_Region_B)
	Log_Summary_share_B = "，带宽更大为：："+ Larger_share_B
	log_ShareBandwidth(Log_DescribeShare_B,Log_GetMetric_share_B,Log_Judge_share_B,Log_Modifyshare_B,Log_Summary_share_B)
	print(Log_DescribeShare_B,Log_GetMetric_share_B,Log_Judge_share_B,Log_Modifyshare_B,Log_Summary_share_B)
	
	
#定时任务
def main():
	while True:
		modify_udpn()
		modify_sharebandwidth()
		time.sleep(60)
if __name__ == '__main__':
	main()
	
	
	