package main

import (
	"log"
	"os"
	"strconv"

	"api_server/model"

	"github.com/joho/godotenv"
	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	_ "github.com/mattn/go-sqlite3"
)

func main() {
	r := gin.Default()

	r.GET("/price-data/", readPriceData)
	r.GET("/price-data/range/", readPriceDataRange)
	r.Run(":8080")
}


func readPriceData(c *gin.Context) {
	all := dbGetAll()
	c.JSON(200, gin.H{
		"all data": all,
	})
}


func readPriceDataRange(c *gin.Context) {
	start := c.Query("start")
	end := c.Query("end")
	pair := c.Query("pair")

	data := dbGetRangeData(start, end, pair)
	c.JSON(200, gin.H{
		"data": data,
	})
}


func dbInit() (*gorm.DB, error) {
	err := godotenv.Load("../.env")
	if err != nil {
		log.Fatalf("Error loading .env file: %v", err)
	}

	dbURL := os.Getenv("DATABASE_URL")
	db, err := gorm.Open("sqlite3", ".." + dbURL)
	if err != nil {
		return nil, err
	}

	return db, nil
}


func dbGetAll() []model.PriceData {
	db, err := dbInit()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	var all []model.PriceData
	db.Order("id desc").Find(&all)

	return all
}


func dbGetRangeData(start, end, pair string) []model.PriceData {
	db, err := dbInit()
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	var data []model.PriceData
	db = db.Order("id desc")

	if pair != "" {
		db = db.Where("pair = ?", pair)
	}
	
	if start != "" {
		startInt, _ := strconv.Atoi(start)
		db = db.Where("close_time >= ?", startInt)
	}

	if end != "" {
		endInt, _ := strconv.Atoi(end)
		db = db.Where("close_time <= ?", endInt)
	}

	db.Find(&data)

	return data
}