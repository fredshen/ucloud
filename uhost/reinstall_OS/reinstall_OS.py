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

#修改为个人秘钥
pubulicKey = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
privateKey = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"

#对操作系统版本进行选择
tmp_choice_imageId = 100
while tmp_choice_imageId > 5 or tmp_choice_imageId < 1:
	tmp_choice_imageId = int(input("选择需要重装的操作系统版本：\n1:CentOS 7.9\n2:CentOS 8.2\n3:Ubuntu 18.04\n4:Ubuntu 20.04\n5.Windows Server 2016\n\n你的选择是（直接输入数字）："))
	if tmp_choice_imageId == 1:
		imageId = "uimage-naikvu"
		OS = "CentOS 7.9"
	elif tmp_choice_imageId == 2:
		imageId = "uimage-nr0z0a"
		OS = "CentOS 8.2"
	elif tmp_choice_imageId == 3:
		imageId = "uimage-icub4s"
		OS = "Ubuntu 18.04"
	elif tmp_choice_imageId == 4:
		imageId = "uimage-5onxu1"
		OS = "Ubuntu 20.04"
	elif tmp_choice_imageId == 5:
		imageId = "uimage-bxcdmu"
		OS = "Windows Server 2016"
	else:
		print("------------------------------\n输入有误，请重新选择！\n")

#对实力进行关机并重装系统
def main():
	client = Client({
	"region": "cn-sh2",
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": "org-fye3q5",
	"base_url": "https://api.ucloud.cn"
})
	#关机
	try:
		resp = client.uhost().stop_uhost_instance({
			"Zone": "cn-sh2-02",
			"UHostId": "uhost-i46e3kx4upv"
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
	print("正在关机。。。")
	time.sleep(10)
	print("------------------------------\n关机成功，正在重装系统。。。")
	#重装系统
	try:
		resp = client.uhost().reinstall_uhost_instance({
			"Zone": "cn-sh2-02",
			"UHostId": "uhost-i46e3kx4upv",
			"Password": "SSSccc12@",
			"ImageId": imageId
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
		print("------------------------------\n系统重装成功!\n操作系统版本为："+ OS +"\n密码为：SS**2@")

if __name__ == '__main__':
	main()
	