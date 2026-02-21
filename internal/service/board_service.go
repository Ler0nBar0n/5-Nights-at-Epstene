package service

import (
	"5-Nights-at-Epstene/internal/entity"
	"5-Nights-at-Epstene/internal/repository"
	"fmt"
)

type BoardService struct {
	boardRepo      *repository.BoardRepository
	connectionRepo *repository.ConnectionRepository
}

func NewBoardService(bRepo *repository.BoardRepository, cRepo *repository.ConnectionRepository) *BoardService {
	return &BoardService{
		boardRepo:      bRepo,
		connectionRepo: cRepo,
	}
}

// CreateBoard создает доску и сразу назначает создателя админом
func (s *BoardService) CreateBoard(name string, creatorID uint) (*entity.Board, error) {
	// 1. Создаем саму доску
	board := &entity.Board{
		Name:      name,
		CreatorID: creatorID,
	}

	if err := s.boardRepo.Create(board); err != nil {
		return nil, fmt.Errorf("не удалось создать доску: %v", err)
	}

	// 2. Создаем связь: назначаем создателя админом (например, роль 10)
	// В твоей сущности Connection роль по умолчанию 1, давай для админа возьмем 10
	connection := &entity.Connection{
		UserID:  creatorID,
		BoardID: board.ID, // ID заполнится после сохранения доски GORM-ом
		Role:    10,
	}

	if err := s.connectionRepo.Create(connection); err != nil {
		return nil, fmt.Errorf("доска создана, но не удалось назначить владельца: %v", err)
	}

	return board, nil
}

// GetBoardByID получает данные о доске
func (s *BoardService) GetBoardByID(id uint) (*entity.Board, error) {
	board, err := s.boardRepo.GetByID(id)
	if err != nil {
		return nil, fmt.Errorf("доска не найдена: %v", err)
	}
	return board, nil
}

// AddUserToBoard добавляет нового участника на доску (обычный пользователь, роль 1)
func (s *BoardService) AddUserToBoard(boardID uint, userID uint) error {
	connection := &entity.Connection{
		UserID:  userID,
		BoardID: boardID,
		Role:    1, // Обычный участник
	}

	if err := s.connectionRepo.Create(connection); err != nil {
		return fmt.Errorf("не удалось добавить пользователя на доску: %v", err)
	}
	return nil
}
