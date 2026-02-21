package service

import (
	"5-Nights-at-Epstene/internal/entity"
	"5-Nights-at-Epstene/internal/repository"
	"errors"
	"fmt"
)

type TaskService struct {
	taskRepo  *repository.TaskRepository
	boardRepo *repository.BoardRepository
}

func NewTaskService(taskRepo *repository.TaskRepository, boardRepo *repository.BoardRepository) *TaskService {
	return &TaskService{
		taskRepo:  taskRepo,
		boardRepo: boardRepo,
	}
}

// CreateTask создает задачу, предварительно проверив существование доски
func (s *TaskService) CreateTask(task *entity.Task) (*entity.Task, error) {
	// 1. Валидация: проверяем, что контент не пустой
	if task.Content == "" {
		return nil, errors.New("содержание задачи не может быть пустым")
	}

	// 2. Проверка: существует ли доска, на которой создаем задачу
	_, err := s.boardRepo.GetByID(task.BoardID)
	if err != nil {
		return nil, fmt.Errorf("доска с ID %d не найдена", task.BoardID)
	}

	// 3. Сохранение в базу
	if err := s.taskRepo.Create(task); err != nil {
		return nil, fmt.Errorf("ошибка при создании задачи: %v", err)
	}

	return task, nil
}

// GetBoardTasks возвращает список всех задач на конкретной доске
func (s *TaskService) GetBoardTasks(boardID uint) ([]entity.Task, error) {
	tasks, err := s.taskRepo.GetByBoardID(boardID)
	if err != nil {
		return nil, fmt.Errorf("не удалось получить задачи: %v", err)
	}
	return tasks, nil
}

// UpdateStatus меняет статус (например, из 'To Do' в 'Done')
func (s *TaskService) UpdateStatus(taskID uint, newStatus int) (*entity.Task, error) {
	task, err := s.taskRepo.UpdateStatus(newStatus, taskID)
	if err != nil {
		return nil, fmt.Errorf("не удалось обновить статус: %v", err)
	}
	return task, nil
}

// AssignUser назначает исполнителя на задачу
func (s *TaskService) AssignUser(taskID uint, userID *uint) (*entity.Task, error) {
	task, err := s.taskRepo.UpdateAssigneeID(userID, taskID)
	if err != nil {
		return nil, fmt.Errorf("не удалось назначить пользователя: %v", err)
	}
	return task, nil
}
