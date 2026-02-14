package repository

import (
	"5-Nights-at-Epstene/internal/entity"

	"gorm.io/gorm"
)

type UserRepository struct {
	db *gorm.DB
}

func NewUserRepository(db *gorm.DB) *UserRepository {
	return &UserRepository{
		db: db,
	}
}

func (r *UserRepository) Create(user *entity.User) error {
	result := r.db.Create(user)
	return result.Error
}

func (r *UserRepository) GetByLogin(login string) (*entity.User, error) {

	var user entity.User

	err := r.db.Where("login = ?", login).First(&user).Error

	if err != nil {
		return nil, err
	}

	return &user, nil
}

func (r *UserRepository) GetByEmail(email string) (*entity.User, error) {
	var user entity.User

	err := r.db.Where("email = ?", email).First(&user).Error

	if err != nil {
		return nil, err
	}

	return &user, nil
}

func (r *UserRepository) GetByID(ID uint) (*entity.User, error) {
	var user entity.User

	err := r.db.Where("id = ?", ID).Find(&user).Error

	if err != nil {
		return nil, err
	}

	return &user, nil
}

func (r *UserRepository) save(user *entity.User) (*entity.User, error) {
	if err := r.db.Save(user).Error; err != nil {
		return nil, err
	}
	return user, nil
}

func (r *UserRepository) UpdateUser(login string, email string, password string, position int) (*entity.User, error) {

	user, err := r.GetByLogin(login)

	if err != nil {
		return nil, err
	}

	user.Email = email
	user.Password = password
	user.Position = position

	return r.save(user)
}

func (r *UserRepository) UpdateEmail(login string, email string) (*entity.User, error) {

	user, err := r.GetByLogin(login)

	if err != nil {
		return nil, err
	}

	user.Email = email

	return r.save(user)
}

func (r *UserRepository) UpdatePassword(login string, password string) (*entity.User, error) {

	user, err := r.GetByLogin(login)

	if err != nil {
		return nil, err
	}

	user.Password = password

	return r.save(user)
}

func (r *UserRepository) UpdatePosition(login string, position int) (*entity.User, error) {

	user, err := r.GetByLogin(login)

	if err != nil {
		return nil, err
	}

	user.Position = position

	return r.save(user)
}

func (r *UserRepository) DeleteByLogin(login string) error {
	err := r.db.Where("login = ?", login).Delete(&entity.User{}).Error
	return err
}
