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

// UpdateUserRole меняет роль пользователя на доске (например, с участника на админа)
func (s *ConnectionService) UpdateUserRole(boardID, userID uint, newRole int) (*entity.Connection, error) {
	// Используем твой метод из репозитория
	// Напоминаю: проверь в репозитории, чтобы там было присвоение role перед save!
	conn, err := s.connRepo.UpdateRole(newRole, boardID, userID)
	if err != nil {
		return nil, fmt.Errorf("не удалось обновить роль: %v", err)
	}

	// Так как в твоем репозитории UpdateRole не менял поле внутри,
	// добавим это здесь для надежности, если еще не поправил репо:
	conn.Role = newRole

	return conn, nil
}

// RemoveUserFromBoard удаляет доступ пользователя к доске
func (s *ConnectionService) RemoveUserFromBoard(boardID, userID uint) error {
	err := s.connRepo.DeleteByUserIDAndBoardID(boardID, userID)
	if err != nil {
		return fmt.Errorf("не удалось удалить пользователя с доски: %v", err)
	}
	return nil
}

// CheckAccess проверяет, есть ли у пользователя вообще доступ к этой доске
func (s *ConnectionService) CheckAccess(boardID, userID uint) (bool, error) {
	conn, err := s.connRepo.GetByUserIDAndBoardID(boardID, userID)
	if err != nil {
		return false, nil // Если связи нет, значит доступа нет
	}

	if conn == nil {
		return false, nil
	}

	return true, nil
}

// GetUserRole возвращает числовое значение роли пользователя
func (s *ConnectionService) GetUserRole(boardID, userID uint) (int, error) {
	conn, err := s.connRepo.GetByUserIDAndBoardID(boardID, userID)
	if err != nil {
		return 0, errors.New("пользователь не является участником доски")
	}
	return conn.Role, nil
}
