package service

import (
	"5-Nights-at-Epstene/internal/entity"
	"5-Nights-at-Epstene/internal/repository"
	"errors"
	"fmt"

	"golang.org/x/crypto/bcrypt"
)

type UserService struct {
	repo *repository.UserRepository
}

func NewUserService(repo *repository.UserRepository) *UserService {
	return &UserService{repo: repo}
}

func (s *UserService) Register(login, email, password string) (*entity.User, error) {

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, fmt.Errorf("ошибка хэширования: %w", err)
	}

	user := &entity.User{
		Login:    login,
		Email:    email,
		Password: string(hashedPassword),
		Position: 1,
	}

	if err := s.repo.Create(user); err != nil {
		return nil, err
	}
	return user, nil
}

func (s *UserService) Login(login, password string) (*entity.User, error) {
	user, err := s.repo.GetByLogin(login)
	if err != nil {
		return nil, errors.New("пользователь не найден")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)); err != nil {
		return nil, errors.New("неверный пароль")
	}

	return user, nil
}
