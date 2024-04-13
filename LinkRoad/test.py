

# -*- coding: utf-8 -*-
"""
Homepage: https://github.com/ucloud/ucloud-sdk-python3
Examples: https://github.com/ucloud/ucloud-sdk-python3/tree/master/examples
Document: https://docs.ucloud.cn/opensdk-python/README
"""
from ucloud.core import exc
from ucloud.client import Client

#修改为个人秘钥
#账号：it@link-road.com
Pubulic_Key = "4eZBe1MqPe4DGoVXowkRzQCWvNqPWYORa"
Private_Key = "AgflYW5XCrZ8hJrwH8e3dLFSWyIz6hzqIJH7YmC8wwwR"
Project_ID = "org-2xvcdf"#Default

def main():
    client = Client({
    "region": "cn-sh2",
    "public_key": Pubulic_Key,
    "private_key": Private_Key,
    "project_id": Project_ID,
    "base_url": "https://api.ucloud.cn"
})

    try:
        resp = client.uhost().describe_uhost_instance({
			"Zone": "cn-sh2-02"
		
        })
    except exc.UCloudException as e:
        print(e)
    else:
        print(resp)

if __name__ == '__main__':
    main()

print("hello world")