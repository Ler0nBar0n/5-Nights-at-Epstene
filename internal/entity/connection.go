package entity

type Connection struct {
	UserID  uint `gorm:"primaryKey;not null" json:"user_id"`
	BoardID uint `gorm:"primaryKey not null" json:"board_id"`
	Role    int  `gorm:"not null; default:1" json:"role"`
}
