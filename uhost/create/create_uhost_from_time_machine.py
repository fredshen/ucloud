#!/usr/bin/env python3

from ucloud.core import exc
from ucloud.client import Client

#标准配置部分
ucloud_public_key = '68c2VGP58wPHhOpK2tVxQT4C8FaOStqlFFEghhZ1c'
ucloud_private_key = 'IJAlrnXMywlCgHZwa9m9958Ii2n9XIQ2R5kYD5dErKWCCTsHtiAae8GGTk8aaJR8oL'

#输入部分
ucloud_uhost_id = input('请输入原主机的资源ID：')
ucloud_restore_disk_time_stamps = input('请输入要创建主机的备份时间点（UNIX时间戳）：')
ucloud_password = input('请为将要创建新主机设定密码（base64编码）：')
ucloud_restore_disk_id = input('请输入DISKID（例如：6cc9af1a-b985-4382-b0f3-d96ebca0491e）：')

def main():
	client = Client({
		"region": "cn-sh2",
		"project_id": "org-ww0gsd",
		"public_key": ucloud_public_key,
		"private_key": ucloud_private_key,
		"base_url": "https://api.ucloud.cn",
	})
	
	try:
		resp = client.uhost().invoke({
			"Zone": "cn-sh2-02",
			"LoginMode": "Password",
			"UhostID" : ucloud_uhost_id,
			"RestoreDiskIds.n" : ucloud_restore_disk_id,
			"RestoreDiskTimestamps.n" : ucloud_restore_disk_time_stamps,
			"Password" : ucloud_password,
		})
	except exc.UCloudException as e:
		print(e)
	else:
		print(resp)
		
if __name__ == '__main__':
	main()
	

#print time.mktime
		#now = time.mktime(datetime.datetime.now().timetuple())
		#print (now)

		#print (time.time())

		#time.sleep(3)
#print (now)
#print (time.mktime(datetime.datetime.now().timetuple()))