package service

import (
	"5-Nights-at-Epstene/internal/entity"
	"5-Nights-at-Epstene/internal/repository"
	"errors"
)

type RoleService struct {
	roleRepo *repository.RoleRepository
	userRepo *repository.UserRepository
}

func (s *RoleService) CreateSystemRole(operatorID uint, name string, canTasks, canUsers bool) (*entity.Role, error) {
	op, err := s.userRepo.GetByID(operatorID)
	if err != nil || op.Position != 777 {
		return nil, errors.New("только главный админ может создавать системные роли")
	}

	role := &entity.Role{
		Name:           name,
		CanManageTasks: canTasks,
		CanManageUsers: canUsers,
	}
	err = s.roleRepo.Create(role)
	return role, err
}
