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

#基础信息配置
ShareBandwidthId = "bwshare-rqm1w9sttxn"
Region = "cn-sh2"#填写出口大的一端
Project_ID = "org-en5c1p"
Log_Path = "/Users/fredshen/Downloads/uwork/API_test/share_bandwidth.log"
Upper_Limit = 8000#上限值


#请勿随意修改以下内容
Pace = [0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25]

#基础信息
client = Client({
	"region": Region,
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})


def check():
	#获取当前购买带宽值
	try:
		resp1 = client.unet().describe_share_bandwidth({
			"ShareBandwidthIds": [
				ShareBandwidthId
			]
			
		})
#		print(resp1["DataSet"][0].get("ShareBandwidth"))
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp1)
	Current_Bandwith = resp1["DataSet"][0].get("ShareBandwidth")
	Log_describe_share_bandwidth = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  +" "+ShareBandwidthId  +" " + str(resp1["DataSet"][0].get("ShareBandwidth")) +" " + str(resp1.get("Action"))+ " "+str(resp1.get("RetCode"))	#print(Log_GetSimpleUGNBwPackages)
	
	#获取监控值	
	try:
		resp2 = client.invoke("GetMetric", {
			"Region": Region,
			"ProjectId": Project_ID,
			"ResourceType": "sharebandwidth",
			"ResourceId": ShareBandwidthId,
			"TimeRange": 200,
			"MetricName.0": "NetworkOutUsage"
	})
	except exc.RetCodeException as e:
		resp2 = e.json()
	Net_Out = resp2["DataSets"].get("NetworkOutUsage")[-1].get("Value")
	
	try:
		resp3 = client.invoke("GetMetric", {
			"Region": Region,
			"ProjectId": Project_ID,
			"ResourceType": "sharebandwidth",
			"ResourceId": ShareBandwidthId,
			"TimeRange": 200,
			"MetricName.0": "NetworkInUsage"
	})
	except exc.RetCodeException as e:
		resp3 = e.json()
	Net_In = resp3["DataSets"].get("NetworkInUsage")[-1].get("Value")
	if Net_Out > Net_In:
		Current_NetworkOutUsage = Net_Out
	else:
		Current_NetworkOutUsage = Net_In

	Log_GetMetric = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  +" "+ShareBandwidthId +" " + str(resp2["DataSets"].get("NetworkOutUsage")[-1].get("Value"))+" " + str(resp2.get("Action")) + " "+str(resp2.get("RetCode"))	#print(Log_GetMetric)
	
	
	#判断
	if Current_NetworkOutUsage < 60:
		New_Bandwith = int(Current_Bandwith * Pace[0])
		if New_Bandwith < 20:
			New_Bandwith = 20
	elif Current_NetworkOutUsage >= 60 and Current_NetworkOutUsage < 70:
		New_Bandwith = int(Current_Bandwith * Pace[2])
		if New_Bandwith < 20:
			New_Bandwith = 20
	elif Current_NetworkOutUsage >= 70 and Current_NetworkOutUsage < 80:
		New_Bandwith = int(Current_Bandwith * Pace[3])
		if New_Bandwith < 20:
			New_Bandwith = 20
	elif Current_NetworkOutUsage >= 80 and Current_NetworkOutUsage < 90:
		New_Bandwith = int(Current_Bandwith * Pace[5])
	elif Current_NetworkOutUsage >= 90 and Current_NetworkOutUsage < 100:
		New_Bandwith = int(Current_Bandwith * Pace[6])
	elif Current_NetworkOutUsage >= 100 and Current_NetworkOutUsage < 110:
		New_Bandwith = int(Current_Bandwith * Pace[7])
	else:#即：>=110
		New_Bandwith = int(Current_Bandwith * Current_NetworkOutUsage / 100 * Pace[8])
	Log_Judge = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  +" "+ShareBandwidthId +" " + str(round(New_Bandwith/Current_Bandwith,2)) +" " + "Judge" + " "+ "/"	
	
	#调整带宽
	try:
		resp4 = client.unet().resize_share_bandwidth({
			"ShareBandwidth": New_Bandwith,
			"ShareBandwidthId": ShareBandwidthId
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp4)	
	
	Log_resize_share_bandwidth = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  +" "+ShareBandwidthId +" " + str(New_Bandwith)+" " + str(resp4.get("Action"))+ " "+str(resp4.get("RetCode")) 	
	
		
	
	#写日志
	try:
		# 打开文件并设置为追加模式（'a'表示追加）
		with open(Log_Path, 'a') as file:
			# 将内容写入文件中
			file.write(Log_describe_share_bandwidth + "\n")
			file.write(Log_GetMetric + "\n")
			file.write(Log_Judge + "\n")
			file.write(Log_resize_share_bandwidth + "\n")
			
		print("---------带宽调整成功---------")
		print("日志成功写入！")
	except Exception as e:
		print("发生错误：", str(e))
		
	#写时序日志
		#例如：20231207 16:26 资源ID 区域a（高）带宽使用率 当前带宽值 调整带宽值 调整幅度 unxi时间戳 区域a 区域b
	
	#运行打印
	print("当前带宽使用率："+ str(Current_NetworkOutUsage))
	print("当前带宽购买值："+ str(Current_Bandwith))
	print("新购买值："+str(New_Bandwith))
	print("调整幅度为："+str(round(New_Bandwith/Current_Bandwith,2)))
	#print(Log_GetSimpleUGNBwPackages)
	#print(Log_GetMetric)
	#print(Log_Judge)
	#print(Log_ModifyUGNBandwidth)
	

#定时任务
def main():
	while True:
		check()
		time.sleep(60)

if __name__ == "__main__":
	main()