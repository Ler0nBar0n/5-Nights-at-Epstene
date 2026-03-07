package entity

type Connection struct {
	UserID  uint `gorm:"primaryKey;not null" json:"user_id"`
	BoardID uint `gorm:"primaryKey not null" json:"board_id"`
	RoleID  uint `gorm:"not null" json:"role_id"`
	Role    Role `gorm:"foreignKey:RoleID"`
}
