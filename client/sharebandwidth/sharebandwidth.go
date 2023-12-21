package sharebandwidth

import (
	"math"
	"time"

	"github.com/ucloud/ucloud-sdk-go/services/unet"
	"github.com/ucloud/ucloud-sdk-go/ucloud"
	"github.com/ucloud/ucloud-sdk-go/ucloud/auth"
	"github.com/ucloud/ucloud-sdk-go/ucloud/response"
	"go.uber.org/zap"

	"github.com/ilolicon/cloudscaler/client/common"
	"github.com/ilolicon/cloudscaler/util"
)

type ShareBandwidthClient struct {
	*unet.UNetClient
}

func NewShareBandwidthClient(region string) *ShareBandwidthClient {
	cfg := ucloud.NewConfig()
	cfg.Region = region
	cfg.BaseUrl = "https://api.ucloud.cn"

	cred := auth.NewCredential()
	cred.PublicKey = util.MustGetEnv("PUBLIC_KEY")
	cred.PrivateKey = util.MustGetEnv("PRIVATE_KEY")

	return &ShareBandwidthClient{unet.NewClient(&cfg, &cred)}
}

func (*ShareBandwidthClient) ComponentName() string {
	return "ShareBandwidthClient"
}

func (c *ShareBandwidthClient) Region() string {
	return c.GetConfig().Region
}

// 获取所有共享带宽详情
func (c *ShareBandwidthClient) GetShareBandwidth() (*unet.DescribeShareBandwidthResponse, error) {
	req := c.NewDescribeShareBandwidthRequest()
	req.ProjectId = ucloud.String(common.ProjectId)

	return c.DescribeShareBandwidth(req)
}

func (c *ShareBandwidthClient) GetDataSet() ([]unet.UnetShareBandwidthSet, error) {
	resp, err := c.GetShareBandwidth()
	if err != nil {
		return nil, err
	}
	return resp.DataSet, nil
}

func (*ShareBandwidthClient) GetLatestBandIn(resp response.GenericResponse) float64 {
	bandin := resp.GetPayload()["DataSets"].(map[string]interface{})["BandIn"].([]interface{})
	if len(bandin) == 0 {
		return 0
	}
	latest := bandin[len(bandin)-1]
	val := latest.(map[string]interface{})["Value"] // unit: bps
	return val.(float64) / 1024 / 1024
}

func (*ShareBandwidthClient) GetLatestBandOut(resp response.GenericResponse) float64 {
	bandout := resp.GetPayload()["DataSets"].(map[string]interface{})["BandOut"].([]interface{})
	if len(bandout) == 0 {
		return 0
	}
	latest := bandout[len(bandout)-1]
	val := latest.(map[string]interface{})["Value"] // unit: bps
	return val.(float64) / 1024 / 1024
}

// 获取监控带宽值
func (c *ShareBandwidthClient) GetLatestBandwidth(resourceId string) (float64, error) {
	req := c.NewGenericRequest()
	err := req.SetPayload(map[string]interface{}{
		"Action":       "GetMetric",
		"ResourceType": "sharebandwidth",
		"ResourceId":   resourceId,
		"TimeRange":    60, // 默认取最近1分钟的值(1分钟1个)
		"MetricName": []interface{}{
			"BandIn",
			"BandOut",
		},
	})
	if err != nil {
		return 0, err
	}

	resp, err := c.GenericInvoke(req)
	if err != nil {
		return 0, err
	}

	bandin := c.GetLatestBandIn(resp)
	bandout := c.GetLatestBandOut(resp)
	return math.Max(bandin, bandout), nil
}

// SetBandoutRules 传入当前监控带宽值 通过"自定义规则"生成新的带宽值
func (*ShareBandwidthClient) SetBandoutRules(in float64) (out int) {
	in = math.Round(in) // 对传入浮点数进行四舍五入处理
	switch {
	case 0 <= in && in < 15:
		out = 20
	case 15 <= in && in < 100:
		out = int(in) + 5
	case 100 <= in && in < 5000:
		out = int(in + in*0.1)
	case 5000 <= in:
		out = 5000
	}
	return
}

// 修改带宽为指定值
func (c *ShareBandwidthClient) ResizeBandwidth(sharebandwidthId string, bandwidth int) error {
	req := c.NewResizeShareBandwidthRequest()
	req.ProjectId = ucloud.String(common.ProjectId)
	req.ShareBandwidthId = ucloud.String(sharebandwidthId)
	req.ShareBandwidth = ucloud.Int(bandwidth)

	_, err := c.ResizeShareBandwidth(req)
	return err
}

func ShareBandwidthRunner(region string, logger *zap.Logger) {
	client := NewShareBandwidthClient(region)

	for range time.NewTicker(60 * time.Second).C {
		data, err := client.GetDataSet()
		if err != nil {
			logger.Error("GetShareBandwidthData", zap.Error(err))
			continue
		}
		for _, v := range data {
			go common.Executor(v.ShareBandwidthId, client, logger)
		}
	}
}
