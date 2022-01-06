#!/usr/bin/env python
#coding:utf-8
import urllib3
import requests
import urllib
import hashlib
import urlparse
import time,sys,commands


Url =  "https://api.ucloud.cn/?"
def opt(arc,num):
	value = {
		'Action': 'DescribeUHostInstance',
		'ProjectId': 'org-4z25b1',
		'Region': 'cn-bj2',
		'Zone': arc,
	       	'Offset':num,
	        'Limit':100,
	        'IsolationGroup':'',
	        'VPCId':'uvnet-p1crdd',
#	        'SubnetId':'subnet-plk34h'
	}
	return value

tag = ['3001区服','3002区服','3003区服','3006区服','3009区服','3010区服','3012区服','3014区服']
gup = ['cn-bj2-02','cn-bj2-03','cn-bj2-04','cn-bj2-05']


PublicKey = 'TbIknX1Uo5aMLVDZhW8hqL/sk5f99qjJ4d1SjbhLmki7ws2fG9CNEpYT+/8I9CEv'
Privekey = 'yfwPT8EBKSoaM1Dpd+/etjmb6bFuSlsn+Z/dADpC2OZqtdFF1mgs05G6gSSqqykh'

AccessPub = 'TbIknX1Uo5aMLVDZhW8hqL%2Fsk5f99qjJ4d1SjbhLmki7ws2fG9CNEpYT%2B%2F8I9CEv'


def Sigure(public_key,private_key,group,arc,num):
	params = opt(arc,num)
	public_key = {'PublicKey':public_key,'Tag':group}
        items = list(params.items()) + list(public_key.items())
	items.sort()
	params_data = "";
	for key, value in items:
		params_data = params_data + str(key) + str(value)
	params_data = params_data + private_key
 
	sign = hashlib.sha1()
	sign.update(params_data)
	signature = sign.hexdigest()
 
	return signature

def GetHost(public,group,arc,num):
	Sig = Sigure(PublicKey,Privekey,group,arc,num)
	params01 = opt(arc,num)
	Group = {'Tag':group}
	Full = list(params01.items()) + list(Group.items())
	Full.sort()
	http = []
	for kk,vv in Full:
		http.append("%s=%s"%(kk,vv))
	Link = '&'.join(http)
	http_url = Url + Link + '&PublicKey=' + public + '&Signature=' + Sig
	print http_url
	
	GetValue = requests.get(http_url)
	return GetValue.json()

zhu = open('chayi.txt','r')
zlist = []

for env in zhu:
	env = env.replace('\n','')
	zlist.append(env)

for are in tag:
	for gp in gup:
        #ur = Sigure(PublicKey,Privekey,are)
		locat = 0
		Value = GetHost(AccessPub,are,gp,locat)
		count = Value['TotalCount']
		area = int(count) / 100
		if area > 0:
			for kk in range(area+1):
				num1 = kk * 100
				all_value = GetHost(AccessPub,are,gp,num1)
				count1 = all_value['TotalCount']
				gnum = len(all_value['UHostSet'])
				if gnum >= 100:
					for vv in range(100):
						lhost = all_value['UHostSet'][vv]['Name']
						if lhost in zlist:
			 				print all_value['UHostSet'][vv]['UHostId'] +'\t'+ all_value['UHostSet'][vv]['Name']+'\t'+all_value['UHostSet'][vv]['IPSet'][0]['IP']+'\t'+str(all_value['UHostSet'][vv]['CPU'])+'\t'+str(int(Value['UHostSet'][vv]['Memory'])/1024)
							print str(int(Value['UHostSet'][vv]['Memory']))
				else:
					for v1 in range(gnum):
						lhost = all_value['UHostSet'][v1]['Name']
						if lhost in zlist:
							print all_value['UHostSet'][v1]['UHostId'] +'\t'+ all_value['UHostSet'][v1]['Name']+'\t'+all_value['UHostSet'][v1]['IPSet'][0]['IP']+'\t'+str(all_value['UHostSet'][v1]['CPU'])+'\t'+str(int(Value['UHostSet'][v1]['Memory'])/1024)
							print str(int(Value['UHostSet'][v1]['Memory']))
		else:
			for vv in range(count):
				lhost = Value['UHostSet'][vv]['Name']
				if lhost in zlist:
					print Value['UHostSet'][vv]['UHostId'] +'\t'+ Value['UHostSet'][vv]['Name']+'\t'+Value['UHostSet'][vv]['IPSet'][0]['IP']+'\t'+str(Value['UHostSet'][vv]['CPU'])+'\t'+str(int(Value['UHostSet'][vv]['Memory'])/1024)
					print str(int(Value['UHostSet'][vv]['Memory']))
