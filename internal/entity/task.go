package entity

import (
	"time"

	"gorm.io/gorm"
)

type Task struct {
	gorm.Model

	BoardId    uint      `gorm:"not null" json:"board_id"`
	CreatorId  uint      `gorm:"not null" json:"creator_id"`
	AssigneeId *uint     `json:"assignee_id"`
	Content    string    `gorm:"not null" json:"content"`
	Deadline   time.Time `json:"deadline"`
	Color      string    `gorm:"default: #FF0001" json:"color"`
	Status     int       `gorm:"not null; default: 0" json:"status"`
}
