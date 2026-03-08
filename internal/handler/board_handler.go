package handler

import (
	"5-Nights-at-Epstene/internal/dto"
	"5-Nights-at-Epstene/internal/service"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

type BoardHandler struct {
	service *service.BoardService
}

func NewBoardHandler(s *service.BoardService) *BoardHandler {
	return &BoardHandler{service: s}
}

func (h *BoardHandler) Create(c *gin.Context) {
    var req dto.CreateBoardRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Извлекаем ID пользователя, который мы положили в Middleware
    userID := c.MustGet("user_id").(uint) 

    board, err := h.service.CreateBoard(req.Name, userID)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    c.JSON(http.StatusCreated, board)
}

func (h *BoardHandler) GetByID(c *gin.Context) {
	id, _ := strconv.Atoi(c.Param("id"))
	board, err := h.service.GetBoardByID(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Доска не найдена"})
		return
	}
	c.JSON(http.StatusOK, board)
}