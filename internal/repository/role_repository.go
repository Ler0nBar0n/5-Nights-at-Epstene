package repository

import (
	"5-Nights-at-Epstene/internal/entity"

	"gorm.io/gorm"
)

type RoleRepository struct {
	db *gorm.DB
}

func (r *RoleRepository) GetByName(name string) (*entity.Role, error) {
	var role entity.Role
	err := r.db.Where("name = ?", name).First(&role).Error
	return &role, err
}

func (r *RoleRepository) Create(role *entity.Role) error {
	return r.db.Create(role).Error
}
