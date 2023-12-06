#!/usr/bin/env python3

#修改为个人秘钥
#账号：shenchaook@gmail.com
pubulicKey = "4eZBKoQnYDiAjVI6SPmPiRH47Sj4Fhxlu"
privateKey = "9AXyD8mINFgHlrblFp1tAPIcUBwfojXiBKgoPyEzgi6W"


from ucloud.core import exc
from ucloud.client import Client


client = Client({
"public_key": pubulicKey,
"private_key": privateKey,
"project_id": "org-fye3q5",
"base_url": "https://api.ucloud.cn"
})

resp = client.udpn().modify_udpn_bandwidth({
	"UDPNId": "udpn-r3qv8h1dkau",
	"Bandwidth": 3
	
})


print("---------")
print(resp)