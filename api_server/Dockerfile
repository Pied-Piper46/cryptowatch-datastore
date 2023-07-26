FROM golang:1.20

WORKDIR /api_server

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY . .

RUN go get github.com/gin-gonic/gin
RUN go get github.com/jinzhu/gorm
RUN go get github.com/mattn/go-sqlite3
RUN go get github.com/joho/godotenv
RUN go build -o main .

EXPOSE 8080

CMD ["./main"]