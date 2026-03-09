package handler

import (
	"5-Nights-at-Epstene/internal/entity"
	"5-Nights-at-Epstene/internal/service"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

type TaskHandler struct {
	service *service.TaskService
}

func NewTaskHandler(s *service.TaskService) *TaskHandler {
	return &TaskHandler{service: s}
}

// Create godoc
// @Summary Создание задачи
// @Security BearerAuth
// @Tags tasks
// @Accept json
// @Produce json
// @Param input body entity.Task true "Объект задачи"
// @Success 201 {object} entity.Task
// @Router /tasks/ [post]
func (h *TaskHandler) Create(c *gin.Context) {
	var task entity.Task
	if err := c.ShouldBindJSON(&task); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	createdTask, err := h.service.CreateTask(&task)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, createdTask)
}

// GetByBoard godoc
// @Summary Получить все задачи доски
// @Security BearerAuth
// @Tags tasks
// @Param id path int true "Board ID"
// @Success 200 {array} entity.Task
// @Router /boards/{id}/tasks [get]
func (h *TaskHandler) GetByBoard(c *gin.Context) {
	boardID, _ := strconv.Atoi(c.Param("id"))
	tasks, err := h.service.GetBoardTasks(uint(boardID))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, tasks)
}