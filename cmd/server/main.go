package main

// @title 5 Nights at Epstene API
// @version 1.0
// @description API сервера для управления досками и задачами.
// @termsOfService http://swagger.io/terms/

// @contact.name API Support
// @contact.url http://www.swagger.io/support
// @contact.email support@swagger.io

// @license.name Apache 2.0
// @license.url http://www.apache.org/licenses/LICENSE-2.0.html

// @host localhost:8080
// @BasePath /api
// @securityDefinitions.apikey BearerAuth
// @in header
// @name Authorization

import (
	"5-Nights-at-Epstene/internal/database"
	"5-Nights-at-Epstene/internal/handler"
	"5-Nights-at-Epstene/internal/repository"
	"5-Nights-at-Epstene/internal/service"
	"github.com/gin-gonic/gin"

	_ "5-Nights-at-Epstene/docs" 
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

func main() {
   
	db := database.CreationDB()
	database.SeedRoles(db)

	userRepo := repository.NewUserRepository(db)
	boardRepo := repository.NewBoardRepository(db)
	connRepo := repository.NewConnectionRepository(db)
	taskRepo := repository.NewTaskRepository(db)

	userService := service.NewUserService(userRepo)
	boardService := service.NewBoardService(boardRepo, connRepo)
	taskService := service.NewTaskService(taskRepo, boardRepo)

	authHandler := handler.NewAuthHandler(userService)
	boardHandler := handler.NewBoardHandler(boardService)
	taskHandler := handler.NewTaskHandler(taskService)

	r := gin.Default()
    r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler)) 
    api := r.Group("/api")
    {
        auth := api.Group("/auth")
        {
            auth.POST("/register", authHandler.Register)
            auth.POST("/login", authHandler.Login)
        }

        protected := api.Group("/")
        protected.Use(handler.AuthMiddleware()) 
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
