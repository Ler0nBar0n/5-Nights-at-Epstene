package service

import (
	"5-Nights-at-Epstene/internal/entity"
	"5-Nights-at-Epstene/internal/repository"
	"errors"
	"fmt"
)

type ConnectionService struct {
	connRepo *repository.ConnectionRepository
	userRepo *repository.UserRepository
}

func NewConnectionService(cRepo *repository.ConnectionRepository, uRepo *repository.UserRepository) *ConnectionService {
	return &ConnectionService{
		connRepo: cRepo,
		userRepo: uRepo,
	}
}

func (s *ConnectionService) UpdateUserRole(boardID, userID uint, newRole int) (*entity.Connection, error) {
	conn, err := s.connRepo.UpdateRole(newRole, boardID, userID)
	if err != nil {
		return nil, fmt.Errorf("не удалось обновить роль: %v", err)
	}

	return conn, nil
}

func (s *ConnectionService) RemoveUserFromBoard(boardID, userID uint) error {
	err := s.connRepo.DeleteByUserIDAndBoardID(boardID, userID)
	if err != nil {
		return fmt.Errorf("не удалось удалить пользователя с доски: %v", err)
	}
	return nil
}

func (s *ConnectionService) CheckAccess(boardID, userID uint) (bool, error) {
	conn, err := s.connRepo.GetByUserIDAndBoardID(boardID, userID)
	if err != nil {
		return false, nil
	}

	if conn == nil {
		return false, nil
	}

	return true, nil
}

func (s *ConnectionService) GetUserRole(boardID, userID uint) (int, error) {
	conn, err := s.connRepo.GetByUserIDAndBoardID(boardID, userID)
	if err != nil {
		return 0, errors.New("пользователь не является участником доски")
	}
	return int(conn.RoleID), nil
}
