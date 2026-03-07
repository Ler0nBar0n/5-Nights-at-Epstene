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

func (s *BoardService) CreateBoard(name string, creatorID uint) (*entity.Board, error) {
	board := &entity.Board{
		Name:      name,
		CreatorID: creatorID,
	}

	if err := s.boardRepo.Create(board); err != nil {
		return nil, fmt.Errorf("не удалось создать доску: %v", err)
	}

	connection := &entity.Connection{
		UserID:  creatorID,
		BoardID: board.ID,
		RoleID:  uint(10),
	}

	if err := s.connectionRepo.Create(connection); err != nil {
		return nil, fmt.Errorf("доска создана, но не удалось назначить владельца: %v", err)
	}

	return board, nil
}

func (s *BoardService) GetBoardByID(id uint) (*entity.Board, error) {
	board, err := s.boardRepo.GetByID(id)
	if err != nil {
		return nil, fmt.Errorf("доска не найдена: %v", err)
	}
	return board, nil
}

func (s *BoardService) AddUserToBoard(boardID uint, userID uint) error {
	connection := &entity.Connection{
		UserID:  userID,
		BoardID: boardID,
		RoleID:  uint(1),
	}

	if err := s.connectionRepo.Create(connection); err != nil {
		return fmt.Errorf("не удалось добавить пользователя на доску: %v", err)
	}
	return nil
}
