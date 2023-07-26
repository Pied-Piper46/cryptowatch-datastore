package main

import (
	"log"
	"os"

	"api_server/model"

	"github.com/joho/godotenv"
	"github.com/gin-gonic/gin"
	"github.com/jinzhu/gorm"
	_ "github.com/mattn/go-sqlite3"
)

func main() {

	r := gin.Default()

	r.GET("/read/", readAllData)
	r.Run(":8080")
}


func dbGetAll() []model.PriceData {

	err := godotenv.Load("../.env")
	if err != nil {
		log.Fatalf("Error loading .env file: %v", err)
	}

	dbURL := os.Getenv("DATABASE_URL")
	db, err := gorm.Open("sqlite3", ".." + dbURL)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	var all []model.PriceData
	db.Order("id desc").Find(&all)
	db.Close()

	return all
}


func readAllData(c *gin.Context) {
	all := dbGetAll()
	c.JSON(200, gin.H{
		"all data": all,
	})
}