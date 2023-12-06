#!/usr/bin/python3

# -*- coding: UTF-8 -*-
import os
import time
import logging
import logging.handlers
from ucloud.client import Client
from ucloud.core import exc


def get_logger(log_path="../ukdmgr_logs/"):
	file_name = os.path.basename(__file__)
	log_format = '%(asctime)s %(process)d %(filename)s %(lineno)s %(levelname)s %(message)s'
	logger = logging.getLogger(file_name.replace(".py", ""))
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter(log_format)
	
	# 存储日志文件
	loghandler = logging.handlers.RotatingFileHandler(log_path + file_name.replace(".py", ".log"), maxBytes=1024 * 1024 * 100,
														backupCount=3)
	loghandler.setFormatter(formatter)
	loghandler.setFormatter(formatter)
	logger.addHandler(loghandler)
	
	# 控台打印
	streamhandler = logging.StreamHandler()
	streamhandler.setFormatter(formatter)
	logger.addHandler(streamhandler)
	return logger


logger = get_logger()


class ZmUkdUdpnManager(object):
	"""
	manage ucloud udpn
	"""
	
	def __init__(self, ukdkey_info, udpn_info_shkr):
		self.client = Client({
			"project_id": ukdkey_info.get("project_id"),
			"public_key": ukdkey_info.get("public_key"),
			"private_key": ukdkey_info.get("private_key"),
		}, logger=logger)
		self.udpn_resid = udpn_info_shkr.get("udpn_resid")
		self.udpn_region_src = udpn_info_shkr.get("udpn_region_src")
		self.udpn_region_src_bwshare_id = udpn_info_shkr.get("udpn_region_src_bwshare_id")
		self.udpn_region_dest = udpn_info_shkr.get("udpn_region_dest")
		self.udpn_region_dest_bwshare_id = udpn_info_shkr.get("udpn_region_dest_bwshare_id")
		self.udpn_max_bandwidth = udpn_info_shkr.get("udpn_max_bandwidth")
		self.udpn_min_bandwidth = udpn_info_shkr.get("udpn_min_bandwidth")
		
	def get_share_bindwidth_info(self, share_bandwidth_define):
		"""
		根据源或目标获取共享带宽包的区域和
		:param share_bandwidth_region:
		:return: share_bindwidth_info
		"""
		if share_bandwidth_define == "src":
			share_bindwidth_region = self.udpn_region_src
			share_bindwith_id = self.udpn_region_src_bwshare_id
		elif share_bandwidth_define == "dest":
			share_bindwidth_region = self.udpn_region_dest
			share_bindwith_id = self.udpn_region_dest_bwshare_id
		else:
			raise Exception("ukd没有对应的带宽包区域")
		return {"share_bindwidth_region": share_bindwidth_region, "share_bindwith_id": share_bindwith_id}
	
	def get_udpn_bandoutmaxusage(self):
		"""
		获取当前udpn带宽最大使用率
		:return: bandoutmaxusage
		"""
		curr_time = int(time.time())
		data = {
			"Region": self.udpn_region_dest,
			"ResourceType": "udpn",
			"ResourceId": self.udpn_resid,
			"MetricName.0": "BandOutMaxUsage",
			"EndTime": curr_time,
			"BeginTime": curr_time - 60,
		}
		bandoutmaxusage = None
		try:
			resp = self.client.invoke(action="GetMetric", args=data)
			items = resp["DataSets"].get('BandOutMaxUsage')
			bandoutmaxusage = int(items[-1]["Value"])
		except exc.RetCodeException as e:
			logger.error("获取UDPN带宽使用率失败1")
			logger.error(e)
		except Exception as e:
			logger.error("获取UDPN带宽使用率失败2")
			logger.error(e)
		return bandoutmaxusage
	
	def get_udpn_bandwidth(self):
		"""
		获取当前udpn设置的最大带宽值
		:return: bandwidth
		"""
		bandwidth = None
		try:
			resp = self.client.udpn().describe_udpn({
				"UDPNId": self.udpn_resid
			})
			bandwidth = resp.get("DataSet")[0].get("Bandwidth")
		except exc.UCloudException as e:
			logger.error("获取UDPN带宽值失败1")
			logger.error(e)
		except Exception as e:
			logger.error("获取UDPN带宽值失败2")
			logger.error(e)
		return bandwidth
	
	def get_udpn_sharebandwidth(self, share_bandwidth_define):
		"""
		获取udpn各区域共享带宽包的带宽大小
		:param share_bandwidth_define:
		:return:
		"""
		share_bindwidth_info = self.get_share_bindwidth_info(share_bandwidth_define)
		sharebandwidth = None
		try:
			resp = self.client.unet().describe_share_bandwidth({
				"Region": share_bindwidth_info.get("share_bindwidth_region"),
				"ShareBandwidthIds": [share_bindwidth_info.get("share_bindwith_id")],
			})
			sharebandwidth = resp.get("DataSet")[0].get("ShareBandwidth")
		except exc.UCloudException as e:
			logger.error("获取UDPN共享带宽包值失败1")
			logger.error(e)
		except Exception as e:
			logger.error("获取UDPN共享带宽包值失败2")
			logger.error(e)
		return sharebandwidth
	
	def set_udpn_bandwidth(self, expect_bandwidth):
		"""
		设置udpn最大带宽
		:param expect_bandwidth:
		:return:
		"""
		try:
			self.client.udpn().modify_udpn_bandwidth({
				"UDPNId": self.udpn_resid,
				"Bandwidth": expect_bandwidth
			})
		except exc.UCloudException as e:
			logger.error("设置UDPN带宽值失败1")
			logger.error(e)
		except Exception as e:
			logger.error("设置UDPN带宽值失败2")
			logger.error(e)
			
	def set_udpn_share_bandwidth(self, expect_bandwidth, share_bandwidth_define):
		"""
		设置udpn共享带宽包的最大带宽
		:param expect_bandwidth:
		:param share_bandwidth_define:
		:return:
		"""
		share_bindwidth_info = self.get_share_bindwidth_info(share_bandwidth_define)
		try:
			self.client.unet().resize_share_bandwidth({
				"Region": share_bindwidth_info.get("share_bindwidth_region"),
				"ShareBandwidthId": share_bindwidth_info.get("share_bindwith_id"),
				"ShareBandwidth": expect_bandwidth
			})
		except exc.UCloudException as e:
			logger.error("设置UDPN共享带宽包值失败1")
			logger.error(e)
		except Exception as e:
			logger.error("设置UDPN共享带宽包值失败1")
			logger.error(e)
			
	def set_bandwidth_share_and_udpn(self, set_bandwidth):
		"""
		设置udpn的最大带宽，设置udpn的源和目的的共享带宽包的最大带宽
		:param set_bandwidth:
		:return:
		"""
		if set_bandwidth > self.udpn_max_bandwidth:
			set_bandwidth = self.udpn_max_bandwidth
			logger.warning("带宽已达到最大值,无法继续设置,设置带宽为最大值")
		if set_bandwidth < self.udpn_min_bandwidth:
			set_bandwidth = self.udpn_min_bandwidth
			logger.warning("带宽已达到最小值,无法继续设置,设置带宽为最小值")
		self.set_udpn_bandwidth(set_bandwidth)
		self.set_udpn_share_bandwidth(set_bandwidth, "src")
		self.set_udpn_share_bandwidth(set_bandwidth, "dest")
		return set_bandwidth
	
	
	def increase_bandwidth(self, increase_utilization, udpn_bandwidth_rate, current_bandwidth):
		"""
		增长udpn最大带宽
		:param increase_utilization:
		:param udpn_bandwidth_rate:
		:param current_bandwidth:
		:return:
		"""
		set_bandwidth = current_bandwidth + (current_bandwidth * increase_utilization)
		set_bandwidth = self.set_bandwidth_share_and_udpn(set_bandwidth)
		logger.warning(
			f"UDPN的当前设置最大带宽为: {current_bandwidth} 当前带宽使用率为: {udpn_bandwidth_rate} 设置新的最大带宽为: {set_bandwidth} 当前带宽增长: {increase_utilization}")
		
	def decrease_bandwidth(self, decrease_utilization, udpn_bandwidth_rate, current_bandwidth):
		"""
		降低udpn最大带宽
		:param decrease_utilization:
		:param udpn_bandwidth_rate:
		:param current_bandwidth:
		:return:
		"""
		set_bandwidth = current_bandwidth - (current_bandwidth * decrease_utilization)
		set_bandwidth = self.set_bandwidth_share_and_udpn(set_bandwidth)
		logger.warning(
			f"UDPN的当前设置最大带宽为: {current_bandwidth} 当前带宽使用率为: {udpn_bandwidth_rate} 设置新的最大带宽为: {set_bandwidth} 当前带宽下降: {decrease_utilization}")
		
	def set_bandwidth_interval_rate(self, udpn_bandwidth_rate, current_bandwidth, crease_rate):
		if udpn_bandwidth_rate >= 130:
			self.increase_bandwidth(crease_rate[0], udpn_bandwidth_rate, current_bandwidth)
		if udpn_bandwidth_rate >= 100 and udpn_bandwidth_rate < 130:
			self.increase_bandwidth(crease_rate[1], udpn_bandwidth_rate, current_bandwidth)
		if udpn_bandwidth_rate >= 85 and udpn_bandwidth_rate < 100:
			self.increase_bandwidth(crease_rate[2], udpn_bandwidth_rate, current_bandwidth)
		if udpn_bandwidth_rate >= 65 and udpn_bandwidth_rate < 75:
			self.decrease_bandwidth(crease_rate[3], udpn_bandwidth_rate, current_bandwidth)
		if udpn_bandwidth_rate >= 55 and udpn_bandwidth_rate < 65:
			self.decrease_bandwidth(crease_rate[4], udpn_bandwidth_rate, current_bandwidth)
		if udpn_bandwidth_rate >= 35 and udpn_bandwidth_rate < 55:
			self.decrease_bandwidth(crease_rate[5], udpn_bandwidth_rate, current_bandwidth)
		if udpn_bandwidth_rate <= 35 and udpn_bandwidth_rate > 0:
			self.decrease_bandwidth(crease_rate[6], udpn_bandwidth_rate, current_bandwidth)
			
	def set_bandwidth_interval(self, current_bandwidth, udpn_bandwidth_rate):
		if current_bandwidth >= 0 and current_bandwidth <= 100:
			crease_rate = [0.6, 0.5, 0.4, 0.3, 0.1, 0.2, 0.3]
			self.set_bandwidth_interval_rate(udpn_bandwidth_rate, current_bandwidth, crease_rate)
		elif current_bandwidth > 100 and current_bandwidth <= 300:
			crease_rate = [0.6, 0.5, 0.4, 0.3, 0.1, 0.2, 0.3]
			self.set_bandwidth_interval_rate(udpn_bandwidth_rate, current_bandwidth, crease_rate)
		elif current_bandwidth > 300 and current_bandwidth <= 500:
			crease_rate = [0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4]
			self.set_bandwidth_interval_rate(udpn_bandwidth_rate, current_bandwidth, crease_rate)
		elif current_bandwidth > 500 and current_bandwidth <= 800:
			crease_rate = [0.2, 0.12, 0.08, 0.05, 0.1, 0.15, 0.2]
			self.set_bandwidth_interval_rate(udpn_bandwidth_rate, current_bandwidth, crease_rate)
		else:
			crease_rate = [0.15, 0.1, 0.05, 0.05, 0.1, 0.15, 0.2]
			self.set_bandwidth_interval_rate(udpn_bandwidth_rate, current_bandwidth, crease_rate)
			
	def auto_set_udpn_bandwidth_line(self):
		"""
		根据当前udpn使用的比率自动设置udpn带宽
		:return:
		"""
		udpn_bandwidth_rate = self.get_udpn_bandoutmaxusage()
		current_bandwidth = self.get_udpn_bandwidth()
		if current_bandwidth is None:
			pass
		else:
			self.set_bandwidth_interval(current_bandwidth, udpn_bandwidth_rate)
			
def op_udpn_mgr_shjp():
	ukdkey_info = {
		"project_id": "xxx",
		"public_key": "xxx",
		"private_key": "xxx"
	}
	
	udpn_info_shjp = {
		"udpn_resid": "xxx",
		"udpn_region_src": "cn-sh2",
		"udpn_region_src_bwshare_id": "xxx",
		"udpn_region_dest": "kr-seoul",
		"udpn_region_dest_bwshare_id": "xxx",
		"udpn_min_bandwidth": 20,
		"udpn_max_bandwidth": 1000
	}
	opudpnmgr = ZmUkdUdpnManager(ukdkey_info, udpn_info_shjp)
	opudpnmgr.auto_set_udpn_bandwidth_line()
	
	
def main():
	while True:
		op_udpn_mgr_shjp()
		time.sleep(60)
		
		
if __name__ == '__main__':
	main()