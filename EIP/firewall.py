from ucloud.core import exc
from ucloud.client import Client
import pandas as pd
import json

ucloud_public_key = '******************'
ucloud_private_key = '******************'

'''
解析原有的规则
'''
def resolve_describe_json(response_string):
    if response_string:
        try:
            rule_list=response_string['DataSet'][0]['Rule']
            rule_string_list=[]
            for rule in rule_list:
                rule_string_list.append(rule['ProtocolType']+'|'+rule['DstPort']+'|'+rule['SrcIP']+'|'+rule['RuleAction']+'|'+rule['Priority']+'|'+rule['Remark'])
            return rule_string_list
        except Exception as e:
            print(e)
            return []
    else:
        return []
'''
获取原有的规则信息
fwid为比传
'''
def describe_firewall(FWId, region='cn-sh2', project_id='org-lnrov4'):
    client = Client({
        "region": region,
        "project_id": project_id,
        "public_key": ucloud_public_key,
        "private_key": ucloud_private_key,
        "base_url": "https://api.ucloud.cn",
    })

    try:
        resp = client.unet().describe_firewall({
            "FWId": FWId
        })
        return resp

    except exc.UCloudException as e:
        print(e)
'''
更新规则
'''
def update_firewall(FWId, Rule, region='cn-sh2', project_id='org-lnrov4'):
    client = Client({
        "region": region,
        "project_id": project_id,
        "public_key": ucloud_public_key,
        "private_key": ucloud_private_key,
        "base_url": "https://api.ucloud.cn",
    })
    try:
        resp = client.unet().update_firewall({
            "FWId": FWId,
            "Rule": Rule
        })
    except exc.UCloudException as e:
        print(e)
'''
遍历id_list.csv文件，读取fwid去更新规则
operators为默认参数，默认为add，即在原有的规则上新增，当operator传其他值时，将覆盖原有的规则
'''
def main(new_rule,operator='add'):
    df = pd.read_csv('id_list.csv')
    for index, row in df.iterrows():
        fwid = row['FWID']
        rules=[]
        if operator=='add':
            old_rules=resolve_describe_json(describe_firewall(fwid))
            rules.extend(old_rules)
        rules.extend(new_rule)
        update_firewall(fwid,rules)
        print(fwid+'的规则更新完成！')

if __name__ == '__main__':
    rules=[
        'TCP|6789|123.123.123.123|ACCEPT|HIGH|API_TESTING'
    ]
    main(rules)