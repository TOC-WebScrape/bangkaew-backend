package main

import (
	"app_go/handler"
	"fmt"
	"log"
	"net/http"
)

func main() {
	fmt.Println("Starting server at port 5000")
	setRouter()
	if err := http.ListenAndServe(":5000", nil); err != nil {
		log.Fatal(err)
	}
}

func setRouter() {
	fileServer := http.FileServer(http.Dir("./static"))
	http.Handle("/", fileServer)
	http.HandleFunc("/hello", handler.HelloHandler)
	http.HandleFunc("/ws", handler.SocketHandler)
}
