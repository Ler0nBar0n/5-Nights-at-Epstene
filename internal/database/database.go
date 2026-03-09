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
		&entity.Role{},
	)

	return DB
}

func SeedRoles(db *gorm.DB) {
	roles := []entity.Role{
		{Model: gorm.Model{ID: 1}, Name: "Участник", CanManageTasks: false, CanManageUsers: false},
		{Model: gorm.Model{ID: 10}, Name: "Владелец", CanManageTasks: true, CanManageUsers: true},
		{Model: gorm.Model{ID: 100}, Name: "Дедушка Эпштейн", CanManageTasks: true, CanManageUsers: true},
	}

	for _, r := range roles {
		db.FirstOrCreate(&r, entity.Role{Name: r.Name})
	}
}
