package dto

type RegisterRequest struct {
	Login    string `json:"login" validate:"required,min=3,max=30"`
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required,min=6"`
}

type LoginRequest struct {
	Login    string `json:"login" validate:"required"`
	Password string `json:"password" validate:"required"`
}

type UserResponse struct {
	ID       uint   `json:"id"`
	Login    string `json:"login"`
	Email    string `json:"email"`
	Position int    `json:"position"`
}