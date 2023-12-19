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
import json

#修改为个人秘钥
#账号：1349826830@qq.com
Pubulic_Key = "2DVUfAN0VeWFBIV3OBjn9W9tWB5VqB7iOIN9OVuX7"
Private_Key = "FNoqMqrZqMY5mGpOFeudMzF8EfCtcvq838jVLBmOXavkFzkXlX3NjCE5Mf5OUmrwdf"

#基础信息配置
#基础信息配置
#Package_ID = "bw-qv7mfeyujk3"
#UGN_ID = "ugn-qr34zqz4xuh"
Project_ID = "org-en5c1p"
Log_Path = "/Users/fredshen/Downloads/uwork/API_test"

#填写基础信息
print("第一步：创建UDPN")
tmp_choice_peer1 = 100
tmp_choice_peer2 = 100
while tmp_choice_peer1 > 3 or tmp_choice_peer1 < 1:
	tmp_choice_peer1 = int(input("选择UDPN的A端区域：\n1:北京\n2:上海\n3:广州\n你的选择是（直接输入数字）："))
	if tmp_choice_peer1 == 1:
		Region_A = "cn-bj2"
	elif tmp_choice_peer1 == 2:
		Region_A = "cn-sh2"
	elif tmp_choice_peer1 == 3:
		Region_A = "cn-gd"
	else:
		print("------------------------------\n输入有误，请重新选择！\n")
while tmp_choice_peer2 > 8 or tmp_choice_peer1 < 1:
	tmp_choice_peer2 = int(input("选择UDPN的B端区域：\n1:香港\n2:日本\n3:首尔\n4:台北\n5:法兰克福\n6:洛杉矶\n7:新加坡\n你的选择是（直接输入数字）："))
	if tmp_choice_peer2 == 1:
		Region_B = "hk"
	elif tmp_choice_peer2 == 2:
		Region_B = "jpn-tky"
	elif tmp_choice_peer2 == 3:
		Region_B = "kr-seoul"
	elif tmp_choice_peer2 == 4:
		Region_B = "tw-tp"
	elif tmp_choice_peer2 == 5:
		Region_B = "ge-fra"
	elif tmp_choice_peer2 == 6:
		Region_B = "us-ca"
	elif tmp_choice_peer2 == 7:
		Region_B = "sg"
	else:
		print("------------------------------\n输入有误，请重新选择！\n")

#通用接口信息填写
client = Client({
	"region": Region_A,
	"public_key": Pubulic_Key,
	"private_key": Private_Key,
	"project_id": Project_ID,
	"base_url": "https://api.ucloud.cn"
})

#create UDPN

resp = client.udpn().allocate_udpn({
	"Peer1": Region_A,
	"Peer2": Region_B,
	"Bandwidth": 2,
	"ChargeType": "Dynamic"
	})
print(resp)

udpn_id = resp.get("UDPNId",[])
print("------------------------------\n区域为：" + Region_A + "至"+  Region_B +"\nUDPN ID:" + udpn_id)
	
#log_file1 = open('/Users/fredshen/Downloads/uwork/lab/logs/udpn_test/udpn_test.log','a',encoding='utf-8')
#log_file1.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
#log_file1.write(" created " + Region_A + " " + Region_B + " " + udpn_id)
	
#describe_vpc


#create_vpc_intercom
#https://console.ucloud.cn/uapi/detail?id=CreateVPCIntercom

#匹配镜像ID,firewall,password,
if Region_A == "cn_gd":
	Image = "uimage-nk1npr"
	Zone = "cn-gd-02"
	

#create_uhost_instance
	
#create_eip
	
#bind_eip

#print_information
	