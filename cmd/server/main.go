package main

import (
	"5-Nights-at-Epstene/internal/database"
	"fmt"
)

func main() {
	// Запускаем подключение
	db := database.CreationDB()

	if db != nil {
		fmt.Println("Добро пожаловать к дедушке Эпштейну")
	}
}
