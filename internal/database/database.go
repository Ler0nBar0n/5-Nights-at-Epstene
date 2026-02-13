package database

import (
	"5-Nights-at-Epstene/internal/entity"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func CreationDB() *gorm.DB {
	connectingPort := "host=localhost user=postgres password=12345 dbname=fivenightsatepstein port=5432 sslmode=disable"

	DB, Error := gorm.Open(postgres.Open(connectingPort), &gorm.Config{})

	if Error != nil {
		panic(Error)
	}

	DB.AutoMigrate(
		&entity.Board{},
		&entity.Connection{},
		&entity.Task{},
		&entity.User{},
	)

	return DB
}
