print('hello world')
# -*- coding: utf-8 -*-

"""
	Homepage: https://github.com/ucloud/ucloud-sdk-python3
	Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
	Documentation: https://ucloud.github.io/ucloud-sdk-python3/
"""

from ucloud.core import exc
from ucloud.client import Client

ucloud_public_key='68c2VGP58wPHhOpK2tVxQT4C8FaOStqlFFEghhZ1c'
ucloud_private_key='IJAlrnXMywlCgHZwa9m9958Ii2n9XIQ2R5kYD5dErKWCCTsHtiAae8GGTk8aaJR8oL'

def main():
	client = Client({
		"region": "cn-sh2",
		"project_id": "org-ww0gsd",
		"public_key": ucloud_public_key,
		"private_key": ucloud_private_key,
		"base_url": "https://api.ucloud.cn",
	})

	try:
		resp = client.unet().describe_firewall({
			"FWId": "firewall-hsplijea"
		
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)

if __name__ == '__main__':
	main()
