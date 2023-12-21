package account

import (
	"github.com/ucloud/ucloud-sdk-go/services/uaccount"
	"github.com/ucloud/ucloud-sdk-go/ucloud"
	"github.com/ucloud/ucloud-sdk-go/ucloud/auth"

	"github.com/ilolicon/cloudscaler/client/common"
	"github.com/ilolicon/cloudscaler/util"
)

type AccountClient struct {
	projectId string
	client    *uaccount.UAccountClient
}

func NewAccountClient() *AccountClient {
	cfg := ucloud.NewConfig()
	cfg.BaseUrl = "https://api.ucloud.cn"

	cred := auth.NewCredential()
	cred.PublicKey = util.MustGetEnv("PUBLIC_KEY")
	cred.PrivateKey = util.MustGetEnv("PRIVATE_KEY")

	return &AccountClient{
		projectId: common.ProjectId,
		client:    uaccount.NewClient(&cfg, &cred),
	}
}

func (c *AccountClient) GetRegion() (*uaccount.GetRegionResponse, error) {
	req := c.client.NewGetRegionRequest()
	return c.client.GetRegion(req)
}

// 获取所有REGION 若出错则PANIC
func (c *AccountClient) MustGetUniqRegion() map[string]struct{} {
	resp, err := c.GetRegion()
	if err != nil {
		panic(err)
	}

	res := make(map[string]struct{})
	for _, v := range resp.Regions {
		res[v.Region] = struct{}{}
	}
	return res
}
