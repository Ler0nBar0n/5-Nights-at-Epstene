package dto

type CreateRoleRequest struct {
	Name           string `json:"name" validate:"required"`
	CanManageTasks bool   `json:"can_manage_tasks"`
	CanDeleteTasks bool   `json:"can_delete_tasks"`
	CanManageUsers bool   `json:"can_manage_users"`
}