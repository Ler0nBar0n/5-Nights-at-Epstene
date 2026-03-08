package auth

import (
	"time"
	"github.com/golang-jwt/jwt/v5"
)

var secretKey = []byte("super_secret_key_epstene")

func GenerateToken(userID uint, position int) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"user_id":  userID,
		"position": position,
		"exp":      time.Now().Add(time.Hour * 72).Unix(),
	})

	return token.SignedString(secretKey)
}