package entity

import (
	"gorm.io/gorm"
)

type Board struct {
	gorm.Model

	Name      string `gorm:"type:varchar(100);not null;unique" json:"name"`
	CreatorID uint   `json:"creator_id"`
}
