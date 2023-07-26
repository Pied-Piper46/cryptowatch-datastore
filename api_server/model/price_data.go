package model

type PriceData struct {
	ID int
	CloseTime int
	ChartSec int
	Pair string
	Open float64
	High float64
	Low float64
	Close float64
	Volume float64
}