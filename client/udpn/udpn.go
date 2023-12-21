package udpn

import (
	"errors"
	"math"
	"time"

	"github.com/ucloud/ucloud-sdk-go/services/udpn"
	"github.com/ucloud/ucloud-sdk-go/ucloud"
	"github.com/ucloud/ucloud-sdk-go/ucloud/auth"
	"go.uber.org/zap"

	"github.com/ilolicon/cloudscaler/client/common"
	"github.com/ilolicon/cloudscaler/util"
)

type UDPNClient struct {
	*udpn.UDPNClient
}

func NewUDPNClient(region string) *UDPNClient {
	cfg := ucloud.NewConfig()
	cfg.Region = region
	cfg.BaseUrl = "https://api.ucloud.cn"

	cred := auth.NewCredential()
	cred.PublicKey = util.MustGetEnv("PUBLIC_KEY")
	cred.PrivateKey = util.MustGetEnv("PRIVATE_KEY")

	return &UDPNClient{udpn.NewClient(&cfg, &cred)}
}

func (*UDPNClient) ComponentName() string {
	return "UDPNClient"
}

func (c *UDPNClient) Region() string {
	return c.GetConfig().Region
}

// 获取所有UDPN详情
func (c *UDPNClient) GetUDPN() (*udpn.DescribeUDPNResponse, error) {
	req := c.NewDescribeUDPNRequest()
	req.ProjectId = ucloud.String(common.ProjectId)
	req.Offset = ucloud.Int(0)
	req.Limit = ucloud.Int(100)

	return c.DescribeUDPN(req)
}

func (c *UDPNClient) GetDataSet() ([]udpn.UDPNData, error) {
	resp, err := c.GetUDPN()
	if err != nil {
		return nil, err
	}
	return resp.DataSet, nil
}

// 获取监控带宽值
func (c *UDPNClient) GetLatestBandwidth(resourceId string) (float64, error) {
	req := c.NewGenericRequest()
	err := req.SetPayload(map[string]interface{}{
		"Action":       "GetMetric",
		"ResourceType": "udpn",
		"ResourceId":   resourceId,
		"TimeRange":    60, // 默认取最近1分钟的值(1分钟1个)
		"MetricName": []interface{}{
			"BandOutMax",
		},
	})
	if err != nil {
		return 0, err
	}

	resp, err := c.GenericInvoke(req)
	if err != nil {
		return 0, err
	}

	bandout := resp.GetPayload()["DataSets"].(map[string]interface{})["BandOutMax"].([]interface{})
	if len(bandout) == 0 {
		return 0, errors.New("empty DataSets")
	}
	// 获取最新的一个监控值
	latest := bandout[len(bandout)-1]
	val := latest.(map[string]interface{})["Value"] // unit: bps
	return val.(float64) / 1024 / 1024, nil
}

// SetBandoutRules 传入当前监控带宽值 通过"自定义规则"生成新的带宽值
func (*UDPNClient) SetBandoutRules(in float64) (out int) {
	in = math.Round(in) // 对传入浮点数进行四舍五入处理
	switch {
	case 0 <= in && in < 2:
		out = 2
	case 2 <= in && in < 20:
		out = int(in) + 5
	case 20 <= in && in < 100:
		out = int(in) + 10
	case 100 <= in && in < 1000:
		out = int(in + in*0.1)
	case 1000 <= in:
		out = 1000
	}
	return
}

// 修改带宽为指定值
func (c *UDPNClient) ResizeBandwidth(udpnId string, bandwidth int) error {
	req := c.NewModifyUDPNBandwidthRequest()
	req.ProjectId = ucloud.String(common.ProjectId)
	req.UDPNId = ucloud.String(udpnId)
	req.Bandwidth = ucloud.Int(bandwidth)

	_, err := c.ModifyUDPNBandwidth(req)
	return err
}

func UDPNRunner(logger *zap.Logger) {
	client := NewUDPNClient("cn-gd")

	for range time.NewTicker(60 * time.Second).C {
		data, err := client.GetDataSet()
		if err != nil {
			logger.Error("GetUDPNData", zap.Error(err))
			continue
		}
		for _, v := range data {
			go common.Executor(v.UDPNId, NewUDPNClient(v.Peer2), logger)
		}
	}
}
