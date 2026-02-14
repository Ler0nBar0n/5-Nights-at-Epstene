package repository

import (
	"5-Nights-at-Epstene/internal/entity"
	"time"

	"gorm.io/gorm"
)

type TaskRepository struct {
	db *gorm.DB
}

func NewTaskRepository(db *gorm.DB) *TaskRepository {
	return &TaskRepository{
		db: db,
	}
}

func (r *TaskRepository) Create(task *entity.Task) error {
	result := r.db.Create(task)
	return result.Error
}

func (r *TaskRepository) GetByAssigneeID(assigneeID *uint) ([]entity.Task, error) {
	var tasks []entity.Task

	err := r.db.Where("assignee_id = ?", assigneeID).Find(&tasks).Error

	if err != nil {
		return nil, err
	}

	return tasks, nil
}

func (r *TaskRepository) GetByBoardID(boardID uint) ([]entity.Task, error) {
	var tasks []entity.Task

	err := r.db.Where("board_id = ?", boardID).Find(&tasks).Error

	if err != nil {
		return nil, err
	}

	return tasks, nil
}

func (r *TaskRepository) GetByID(ID uint) (*entity.Task, error) {
	var task entity.Task

	err := r.db.Where("id = ?", ID).First(&task).Error

	if err != nil {
		return nil, err
	}

	return &task, nil
}

func (r *TaskRepository) save(task *entity.Task) (*entity.Task, error) {
	if err := r.db.Save(task).Error; err != nil {
		return nil, err
	}
	return task, nil
}

func (r *TaskRepository) UpdateColor(color string, ID uint) (*entity.Task, error) {
	task, err := r.GetByID(ID)

	if err != nil {
		return nil, err
	}

	task.Color = color

	return r.save(task)
}

func (r *TaskRepository) UpdateContent(content string, ID uint) (*entity.Task, error) {
	task, err := r.GetByID(ID)

	if err != nil {
		return nil, err
	}

	task.Content = content

	return r.save(task)
}

func (r *TaskRepository) UpdateDeadline(deadline time.Time, ID uint) (*entity.Task, error) {
	task, err := r.GetByID(ID)

	if err != nil {
		return nil, err
	}

	task.Deadline = deadline

	return r.save(task)
}

func (r *TaskRepository) UpdateAssigneeID(assigneeID *uint, ID uint) (*entity.Task, error) {
	task, err := r.GetByID(ID)

	if err != nil {
		return nil, err
	}

	task.AssigneeID = assigneeID

	return r.save(task)
}

func (r *TaskRepository) UpdateStatus(status int, ID uint) (*entity.Task, error) {
	task, err := r.GetByID(ID)

	if err != nil {
		return nil, err
	}

	task.Status = status

	return r.save(task)
}

func (r *TaskRepository) DeleteByID(ID uint) error {
	err := r.db.Where("id = ?", ID).Delete(&entity.Task{}).Error
	return err
}
