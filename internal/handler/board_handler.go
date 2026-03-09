package handler

import (
	"5-Nights-at-Epstene/internal/dto"
	"5-Nights-at-Epstene/internal/service"
	"5-Nights-at-Epstene/internal/entity"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

type BoardHandler struct {
	service *service.BoardService
}

// Create godoc
// @Summary Создание новой доски
// @Security BearerAuth
// @Tags boards
// @Accept json
// @Produce json
// @Param input body dto.CreateBoardRequest true "Название доски"
// @Success 201 {object} entity.Board
// @Router /boards/ [post]
func NewBoardHandler(s *service.BoardService) *BoardHandler {
	return &BoardHandler{service: s}
}

func (h *BoardHandler) Create(c *gin.Context) {
    var req dto.CreateBoardRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    userID := c.MustGet("user_id").(uint) 

    var board *entity.Board
    var err error
    
    board, err = h.service.CreateBoard(req.Name, userID)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    c.JSON(http.StatusCreated, board)
}

// GetByID godoc
// @Summary Получить информацию о доске
// @Security BearerAuth
// @Tags boards
// @Param id path int true "Board ID"
// @Success 200 {object} entity.Board
// @Router /boards/{id} [get]
func (h *BoardHandler) GetByID(c *gin.Context) {
	id, _ := strconv.Atoi(c.Param("id"))
	board, err := h.service.GetBoardByID(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Доска не найдена"})
		return
	}
	c.JSON(http.StatusOK, board)
}

// Delete godoc
// @Summary Удаление доски
// @Security BearerAuth
// @Tags boards
// @Param id path int true "Board ID"
// @Success 204 "No Content"
// @Router /boards/{id} [delete]
func (h *BoardHandler) Delete(c *gin.Context) {
    id, _ := strconv.Atoi(c.Param("id"))
    roleID := c.MustGet("role_id").(uint)

    if err := h.service.DeleteBoard(uint(id), roleID); err != nil {
        c.JSON(http.StatusForbidden, gin.H{"error": err.Error()})
        return
    }
    c.Status(http.StatusNoContent)
}