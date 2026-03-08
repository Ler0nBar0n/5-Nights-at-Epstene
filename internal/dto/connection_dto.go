package dto

type AddUserToBoardRequest struct {
	UserID uint `json:"user_id" validate:"required"`
	RoleID uint `json:"role_id" validate:"required"`
}

type UpdateUserRoleRequest struct {
	RoleID uint `json:"role_id" validate:"required"`
}

type ConnectionResponse struct {
	UserID   uint         `json:"user_id"`
	User     UserResponse `json:"user"`    
	BoardID  uint         `json:"board_id"`
	RoleID   uint         `json:"role_id"`
	RoleName string       `json:"role_name"`
}