package udpn

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
		{in: 1.0, expected: 2},
		{in: 2.1, expected: 7},
		{in: 2.5, expected: 8},
		{in: 30.0, expected: 40},
		{in: 100.0, expected: 110},
		{in: 118.0, expected: 129},
		{in: 200.0, expected: 220},
		{in: 1200.0, expected: 1000},
	}

	client := &UDPNClient{}
	for _, test := range tests {
		assert.Equal(test.expected, client.SetBandoutRules(test.in))
	}
}
