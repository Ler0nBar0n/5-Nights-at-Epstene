package auth

import (
	"time"
	"github.com/golang-jwt/jwt/v5"
)

var secretKey = []byte("super_secret_key_epstene")

func GenerateToken(userID uint, position int, roleID uint) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"user_id":  userID,
		"role_id": roleID,
		"position": position,
		"exp":      time.Now().Add(time.Hour * 72).Unix(),
	})

	return token.SignedString(secretKey)
}