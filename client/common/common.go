package common

import (
	"fmt"
	"sync"

	"go.uber.org/zap"
)

const ProjectId = "org-4166"

var (
	locker              sync.RWMutex
	LastResizeBandwidth = make(map[string]int)
)

type ExecClient interface {
	ComponentName() string                      // 组件名称
	Region() string                             // 获取Region
	GetLatestBandwidth(string) (float64, error) // 获取最新一个带宽监控值
	ResizeBandwidth(string, int) error          // 调整带宽
	SetBandoutRules(in float64) (out int)       // 带宽设置规则
}

func Executor(id string, client ExecClient, logger *zap.Logger) {
	// 获取当前监控值
	current, err := client.GetLatestBandwidth(id)
	if err != nil {
		logger.Error("获取监控值失败",
			zap.String("component", client.ComponentName()),
			zap.String("region", client.Region()),
			zap.String("id", id),
			zap.Error(err),
		)
		return
	}
	logger.Info("获取监控值成功",
		zap.String("component", client.ComponentName()),
		zap.String("region", client.Region()),
		zap.String("id", id),
		zap.Float64("bandwidth", current),
	)

	var new int
	key := fmt.Sprintf("%s:%s", client.ComponentName(), id)
	locker.RLock()
	last, ok := LastResizeBandwidth[key]
	locker.RUnlock()
	if current < float64(last) || !ok {
		// 由"当前"带宽值生成需要调整的"新"带宽值
		new = client.SetBandoutRules(current)
	} else {
		// 由"当前"带宽值*1.5再去生成需要调整的"新"带宽值
		new = client.SetBandoutRules(current * 1.5)
	}

	locker.Lock()
	LastResizeBandwidth[key] = new // 更新map
	locker.Unlock()
	logger.Info("带宽值变化",
		zap.String("component", client.ComponentName()),
		zap.String("region", client.Region()),
		zap.String("id", id),
		zap.Float64("before", current),
		zap.Int("after", new),
	)

	// 调整带宽值
	if err = client.ResizeBandwidth(id, new); err != nil {
		logger.Error("调整带宽失败",
			zap.String("component", client.ComponentName()),
			zap.String("region", client.Region()),
			zap.String("id", id),
			zap.Error(err),
		)
		return
	}
	logger.Info("调整带宽成功",
		zap.String("component", client.ComponentName()),
		zap.String("region", client.Region()),
		zap.String("id", id),
		zap.Int("bandwidth", new),
	)
}
