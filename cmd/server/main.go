package main

import (
	"5-Nights-at-Epstene/internal/database"
	"5-Nights-at-Epstene/internal/handler"
	"5-Nights-at-Epstene/internal/repository"
	"5-Nights-at-Epstene/internal/service"
	"github.com/gin-gonic/gin"
)

func main() {
	db := database.CreationDB()
	database.SeedRoles(db)

	// 1. Repositories
	userRepo := repository.NewUserRepository(db)
	boardRepo := repository.NewBoardRepository(db)
	connRepo := repository.NewConnectionRepository(db)
	taskRepo := repository.NewTaskRepository(db)

	// 2. Services
	userService := service.NewUserService(userRepo)
	boardService := service.NewBoardService(boardRepo, connRepo)
	taskService := service.NewTaskService(taskRepo, boardRepo)

	// 3. Handlers
	authHandler := handler.NewAuthHandler(userService)
	boardHandler := handler.NewBoardHandler(boardService)
	taskHandler := handler.NewTaskHandler(taskService)

	r := gin.Default()

    api := r.Group("/api")
    {
        // Публичные роуты (регистрация и логин)
        auth := api.Group("/auth")
        {
            auth.POST("/register", authHandler.Register)
            auth.POST("/login", authHandler.Login)
        }

        // ЗАЩИЩЕННЫЕ РОУТЫ (добавляем Middleware здесь)
        protected := api.Group("/")
        protected.Use(handler.AuthMiddleware()) // <--- ЭТОЙ СТРОКИ У ТЕБЯ НЕ ХВАТАЕТ 
        {
            boards := protected.Group("/boards")
            {
                boards.POST("/", boardHandler.Create)
                boards.GET("/:id", boardHandler.GetByID)
                boards.GET("/:id/tasks", taskHandler.GetByBoard)
            }

            tasks := protected.Group("/tasks")
            {
                tasks.POST("/", taskHandler.Create)
            }
        }
    }

    r.Run(":8080")
}
