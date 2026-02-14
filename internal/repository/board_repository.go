package repository

import (
	"5-Nights-at-Epstene/internal/entity"

	"gorm.io/gorm"
)

type BoardRepository struct {
	db *gorm.DB
}

func NewBoardRepository(db *gorm.DB) *BoardRepository {
	return &BoardRepository{
		db: db,
	}
}

func (r *BoardRepository) Create(board *entity.Board) error {
	result := r.db.Create(board)
	return result.Error
}

func (r *BoardRepository) GetByName(name string) (*entity.Board, error) {
	var board entity.Board

	err := r.db.Where("name = ?", name).First(&board).Error

	if err != nil {
		return nil, err
	}

	return &board, nil
}

func (r *BoardRepository) GetByID(ID uint) (*entity.Board, error) {
	var board entity.Board

	err := r.db.Where("id = ?", ID).First(&board).Error

	if err != nil {
		return nil, err
	}

	return &board, nil
}

func (r *BoardRepository) save(board *entity.Board) (*entity.Board, error) {
	if err := r.db.Save(board).Error; err != nil {
		return nil, err
	}
	return board, nil
}

func (r *BoardRepository) UpdateName(name string, ID uint) (*entity.Board, error) {
	board, err := r.GetByID(ID)
	if err != nil {
		return nil, err
	}

	board.Name = name
	return r.save(board)
}
