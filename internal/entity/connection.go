package entity

type Connection struct {
	UserId  uint `gorm:"primaryKey;not null" json:"user_id"`
	BoardId uint `gorm:"primaryKey not null" json:"board_id"`
	Role    int  `gorm:"not null; default: 1" json:"role"`
}
