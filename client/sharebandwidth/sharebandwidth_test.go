package sharebandwidth

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSetBandoutRules(t *testing.T) {
	assert := assert.New(t)

	tests := []struct {
		in       float64
		expected int
	}{
		{in: 1.0, expected: 20},
		{in: 2.1, expected: 20},
		{in: 2.5, expected: 20},
		{in: 40.0, expected: 45},
		{in: 100.0, expected: 110},
		{in: 118.0, expected: 129},
		{in: 200.0, expected: 220},
		{in: 6000.0, expected: 5000},
	}

	client := &ShareBandwidthClient{}
	for _, test := range tests {
		assert.Equal(test.expected, client.SetBandoutRules(test.in))
	}
}
