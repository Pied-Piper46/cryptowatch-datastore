package model

type PriceData struct {
	ID int `gorm:"column:id;primary_key" json:"id"`
	CloseTime int `gorm:"column:close_time" json:"close_time"`
	ChartSec int `gorm:"column:chart_sec" json:"chart_sec"`
	Pair string `gorm:"column:pair" json:"pair"`
	Open float64 `gorm:"column:open" json:"open"`
	High float64 `gorm:"column:high" json:"high"`
	Low float64 `gorm:"column:low" json:"low"`
	Close float64 `gorm:"column:close" json:"close"`
	Volume float64 `gorm:"column:volume" json:"volume"`
}