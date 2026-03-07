package entity

import "gorm.io/gorm"

type Role struct {
	gorm.Model
	Name    string `gorm:"unique;not null" json:"name"`
	BoardID uint   `json:"board_id"`

	CanManageTasks bool `json:"can_manage_tasks"`
	CanDeleteTasks bool `json:"can_delete_tasks"`
	CanManageUsers bool `json:"can_manage_users"`
}
