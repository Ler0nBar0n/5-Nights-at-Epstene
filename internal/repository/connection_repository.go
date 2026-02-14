package repository

import (
	"5-Nights-at-Epstene/internal/entity"

	"gorm.io/gorm"
)

type ConnectionRepository struct {
	db *gorm.DB
}

func NewConnectionRepository(db *gorm.DB) *ConnectionRepository {
	return &ConnectionRepository{
		db: db,
	}
}

func (r *ConnectionRepository) Create(connection *entity.Connection) error {
	result := r.db.Create(connection)
	return result.Error
}

func (r *ConnectionRepository) GetByUserIDAndBoardID(boardID uint, userID uint) (*entity.Connection, error) {
	var connection entity.Connection

	err := r.db.Where("user_id = ?", userID).Where("board_id = ?", boardID).First(&connection).Error

	if err != nil {
		return nil, err
	}

	return &connection, err
}

func (r *ConnectionRepository) save(connection *entity.Connection) (*entity.Connection, error) {
	if err := r.db.Save(connection).Error; err != nil {
		return nil, err
	}
	return connection, nil
}

func (r *ConnectionRepository) UpdateRole(role int, boardID uint, userID uint) (*entity.Connection, error) {
	connection, err := r.GetByUserIDAndBoardID(boardID, userID)

	if err != nil {
		return nil, err
	}

	return r.save(connection)
}

func (r *ConnectionRepository) DeleteByUserIDAndBoardID(boardID uint, userID uint) error {
	err := r.db.Where("user_id = ?", userID).Where("board_id = ?", boardID).Delete(&entity.Connection{}).Error
	return err
}
