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
代办：
1.getmetric比大小
2.打印时序日志
3.根据带宽大小设定幅度
4.根据灵敏度要求设定幅度
'''


#修改为个人秘钥
#账号：1349826830@qq.com
Pubulic_Key = "2DVUfAN0VeWFBIV3OBjn9W9tWB5VqB7iOIN9OVuX7"
Private_Key = "FNoqMqrZqMY5mGpOFeudMzF8EfCtcvq838jVLBmOXavkFzkXlX3NjCE5Mf5OUmrwdf"

#基础信息配置
Package_ID = "bw-rmq0ks7rv2e"
UGN_ID = "ugn-qr34zqz4xuh"
Region = "cn-gd"#填写出口大的一端
Zone = "cn-gd-02"#填写出口大的一端
Project_ID = "org-en5c1p"
Log_Path = "/Users/fredshen/Downloads/uwork/API_test/ugn_flexible_adjustment_prod.log"
Sensitivity = 2 #灵敏度：推荐填2（1.成本优先、2.成本、业务均衡、3.业务稳定优先）

if Sensitivity == 1:
	Pace = [0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25]
elif Sensitivity ==2:
	Pace = [0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25]
elif Sensitivity ==3:
	Pace = [0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25]
else:
	print("缺少必要信息")

#基础信息
client = Client({
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})


def check():
	#获取当前购买带宽值
	try:
		resp1 = client.invoke("GetSimpleUGNBwPackages", {
			"ProjectId": Project_ID,
			"UGNID": UGN_ID
	})
	except exc.RetCodeException as e:
		resp1 = e.json()
	Current_Bandwith = resp1.get("BwPackages")[-1].get("BandWidth")
	Log_GetSimpleUGNBwPackages = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  +" "+UGN_ID + " "+str(resp1.get("RetCode"))+" " + str(resp1.get("Action")) +" " + str(resp1.get("BwPackages")[-1].get("BandWidth"))+" " + str(resp1.get("BwPackages")[-1].get("RegionA"))+" " + str(resp1.get("BwPackages")[-1].get("RegionB"))
	#print(Log_GetSimpleUGNBwPackages)
	
	#获取监控值
	try:
		resp2 = client.invoke("GetMetric", {
			"Region": Region,
			"Zone": Zone,
			"ProjectId": Project_ID,
			"ResourceType": "ugnbw",
			"ResourceId": Package_ID,
			"TimeRange": 200,
			"MetricName.0": "UgnBWOutPeakUsage"
	})
	except exc.RetCodeException as e:
		resp2 = e.json()
	Current_UgnBWOut_PeakUsage = resp2.get("DataSets").get("UgnBWOutPeakUsage")[-1].get("Value")
	#print(Current_UgnBWOut_PeakUsage)
	Log_GetMetric = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  +" "+UGN_ID + " "+str(resp2.get("RetCode"))+" " + str(resp2.get("Action")) +" " + str(resp2.get("DataSets").get("UgnBWOutPeakUsage")[-1].get("Value"))+" " + str(resp1.get("BwPackages")[-1].get("RegionA"))+" " + str(resp1.get("BwPackages")[-1].get("RegionB"))
	#print(Log_GetMetric)
	
	
	#判断
	if Current_UgnBWOut_PeakUsage < 60:
		New_Bandwith = int(Current_Bandwith * Pace[0])
		if New_Bandwith == 0:
			New_Bandwith = 1
			if New_Bandwith == Current_Bandwith:
				New_Bandwith = Current_Bandwith + 1
		elif New_Bandwith == Current_Bandwith:
			New_Bandwith = Current_Bandwith + 1
	elif Current_UgnBWOut_PeakUsage >= 60 and Current_UgnBWOut_PeakUsage < 70:
		New_Bandwith = int(Current_Bandwith * Pace[2])
		if New_Bandwith == 0:
			New_Bandwith = 1
		elif New_Bandwith == Current_Bandwith:
			New_Bandwith = Current_Bandwith + 1
	elif Current_UgnBWOut_PeakUsage >= 70 and Current_UgnBWOut_PeakUsage < 80:
		New_Bandwith = int(Current_Bandwith * Pace[3])
		if New_Bandwith == 0:
			New_Bandwith = 1
		elif New_Bandwith == Current_Bandwith:
			New_Bandwith = Current_Bandwith + 1
	elif Current_UgnBWOut_PeakUsage >= 80 and Current_UgnBWOut_PeakUsage < 90:
		New_Bandwith = int(Current_Bandwith * Pace[5])
		if New_Bandwith == 0:
			New_Bandwith = 1
		elif New_Bandwith == Current_Bandwith:
			New_Bandwith = Current_Bandwith + 1
	elif Current_UgnBWOut_PeakUsage >= 90 and Current_UgnBWOut_PeakUsage < 100:
		New_Bandwith = int(Current_Bandwith * Pace[6])
		if New_Bandwith == 0:
			New_Bandwith = 1
		elif New_Bandwith == Current_Bandwith:
			New_Bandwith = Current_Bandwith + 1
	elif Current_UgnBWOut_PeakUsage >= 100 and Current_UgnBWOut_PeakUsage < 110:
		New_Bandwith = int(Current_Bandwith * Pace[7])
		if New_Bandwith == 0:
			New_Bandwith = 1
		elif New_Bandwith == Current_Bandwith:
			New_Bandwith = Current_Bandwith + 1
	else:#即：>=110
		New_Bandwith = int(Current_Bandwith * Current_UgnBWOut_PeakUsage * Pace[8] / 100)
		if New_Bandwith == 0:
			New_Bandwith = 1
		elif New_Bandwith == Current_Bandwith:
			New_Bandwith = Current_Bandwith + 1
	Log_Judge = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  +" "+UGN_ID + " "+ "/" +" " + "Judge" +" " + str(round(New_Bandwith/Current_Bandwith,2))+" " + str(resp1.get("BwPackages")[-1].get("RegionA"))+" " + str(resp1.get("BwPackages")[-1].get("RegionB"))	
	
	#调整带宽
	try:
		resp3 = client.invoke("ModifyUGNBandwidth", {
			"ProjectId": Project_ID,
			"PackageID": Package_ID,
			"UGNID": UGN_ID,
			"BandWidth": New_Bandwith
	})
	except exc.RetCodeException as e:
		resp3 = e.json()

	Log_ModifyUGNBandwidth = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  +" "+UGN_ID + " "+str(resp3.get("RetCode"))+" " + str(resp3.get("Action")) +" " + str(New_Bandwith)+" " + str(resp1.get("BwPackages")[-1].get("RegionA"))+" " + str(resp1.get("BwPackages")[-1].get("RegionB"))		
	
	#写日志
	try:
		# 打开文件并设置为追加模式（'a'表示追加）
		with open(Log_Path, 'a') as file:
			# 将内容写入文件中
			file.write(Log_GetSimpleUGNBwPackages + "\n")
			file.write(Log_GetMetric + "\n")
			file.write(Log_Judge + "\n")
			file.write(Log_ModifyUGNBandwidth + "\n")
			
		print("---------带宽调整成功---------")
		print("日志成功写入！")
	except Exception as e:
		print("发生错误：", str(e))
		
	#写时序日志
		#例如：20231207 16:26 资源ID 区域a（高）带宽使用率 当前带宽值 调整带宽值 调整幅度 unxi时间戳 区域a 区域b
	
	#运行打印
	print("当前带宽使用率："+ str(Current_UgnBWOut_PeakUsage))
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