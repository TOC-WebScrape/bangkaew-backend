package handler

import (
	"github.com/gorilla/websocket"
	"log"
	"net/http"
	"strings"
)

var upgrades = websocket.Upgrader{}

func getMessage(input string) string {
	result := strings.Replace(input, " ", "", 1)
	return result
}

func SocketHandler(w http.ResponseWriter, r *http.Request) {
	// Upgrade upgrades the HTTP server connection to the WebSocket protocol.
	conn, err := upgrades.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade failed: ", err)
		return
	}
	defer func(conn *websocket.Conn) {
		err := conn.Close()
		if err != nil {
			log.Print("close socket failed: ", err)
			return
		}
	}(conn)

	// Continuously read and write message
	for {
		mt, message, err := conn.ReadMessage()
		if err != nil {
			log.Println("read failed:", err)
			break
		}
		message = []byte(getMessage(string(message)))
		err = conn.WriteMessage(mt, message)
		if err != nil {
			log.Println("write failed:", err)
			break
		}
	}

}
