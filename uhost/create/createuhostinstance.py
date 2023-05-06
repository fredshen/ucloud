# -*- coding: utf-8 -*-
# CreateUHostInstance
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README

"""
#####################################################################################################
#                                                                                                   #
# Author: F.Shen                                                                                    #
# Version: 1.3                                                                                      #
# Release Date: 05/05/2023                                                                          #
#                                                                                                   #
# Features:                                                                                         #
# 1.通过接口快速创建云主机                                                                              #
# ** Let me know if there are any BUGs | fred.shen@ucloud.cn                                        #
#                                                                                                   #
#####################################################################################################

#####################################################################################################
# ------------Release Note------------                                                              #
# Version:1.0                                                                                       #
# 1.template                                                                                        #
#####################################################################################################

from ucloud.core import exc
from ucloud.client import Client

#初始化配置：
#编辑公钥、私钥https://console.ucloud.cn/uaccount/api_manage
publicKey = "7UhCg2TCZym21Kens32UEOLcTp3vDZkn1KW8hrlTC"
privateKey = "8Is6Vgn11quIuUDxOQz6xqLWVr5Gj8nnfJNH73xTQudV30P1L9kQbBRJIrk2qcAT3J"
imageid = "uimage-buwbes"

#区域选择：
zone_choice = input("请选择区域(输入数字)： 1.曼谷、2.马尼拉")
if zone_choice == "1":
	region = "th-bkk"
	zone = "th-bkk-02"
elif zone_choice == "2":
	region = "ph-mnl"
	zone = "ph-mnl-01"
else:
	print("输入有误，请重新运行")

	
def main():
	client = Client({
	"region": region,
	"public_key": publicKey,
	"private_key": privateKey,
	"project_id": "org-czhc4n",
	"base_url": "https://api.ucloud.cn"
})
	
	try:
		resp = client.uhost().create_uhost_instance({
			"Zone": zone,
			"ImageId": imageid,
			"LoginMode": "Password",
			"Password": "VldOc2IzVmtMbU51",
			"Disks": [
				{
					"IsBoot": "True",
					"Size": 50,
					"Type": "CLOUD_SSD"
				}
			]
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
		
if __name__ == '__main__':
	main()
	