#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client

#修改为个人秘钥
#账号：443726357@qq.com
pubulicKey = "7UhCg2TCZym21Kens32UEOLcTp3vDZkn1KW8hrlTC"
privateKey = "8Is6Vgn11quIuUDxOQz6xqLWVr5Gj8nnfJNH73xTQudV30P1L9kQbBRJIrk2qcAT3J"

print("第一步：创建UDPN")
tmp_choice_peer1 = 100
tmp_choice_peer2 = 100
while tmp_choice_peer1 > 3 or tmp_choice_peer1 < 1 or type(tmp_choice_peer1):
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


def main():
	client = Client({
	"region": Region_A,
	"public_key": pubulicKey,
	"private_key": privateKey,
	"project_id": "org-czhc4n",
	"base_url": "https://api.ucloud.cn"
})
	
	try:
		resp = client.udpn().allocate_udpn({
			"Peer1": Region_A,
			"Peer2": Region_B,
			"Bandwidth": 2,
			"ChargeType": "Dynamic"
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		udpn_id = resp.get("UDPNId",[])
		print("------------------------------\n区域为：" + Region_A + "至"+  Region_B +"\nUDPN ID:" + udpn_id)

		#log_file1 = open('/Users/fredshen/Downloads/uwork/lab/logs/udpn_test.log','a',encoding='utf-8')
		#file1.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))   )
	
if __name__ == '__main__':
	main()
	
	
	
	
'''
def main():
	client = Client({
	"region": "cn-gd",
	"public_key": "Input public key at here",
	"private_key": "Input private key at here",
	"project_id": "org-czhc4n",
	"base_url": "https://api.ucloud.cn"
})
	
	try:
		resp = client.udpn().release_udpn({
			"UDPNId": "udpn_id"
			
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
		
if __name__ == '__main__':
	main()
'''