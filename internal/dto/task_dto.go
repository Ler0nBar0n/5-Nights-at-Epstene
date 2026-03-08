package dto

import "time"

type CreateTaskRequest struct {
	BoardID  uint      `json:"board_id" validate:"required"`
	Content  string    `json:"content" validate:"required,max=500"`
	Deadline time.Time `json:"deadline"`
	Color    string    `json:"color"`
}

type TaskResponse struct {
	ID         uint      `json:"id"`
	BoardID    uint      `json:"board_id"`
	CreatorID  uint      `json:"creator_id"`
	AssigneeID *uint     `json:"assignee_id"`
	Content    string    `json:"content"`
	Deadline   time.Time `json:"deadline"`
	Color      string    `json:"color"`
	Status     int       `json:"status"`
}