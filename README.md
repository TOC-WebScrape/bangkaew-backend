# Bangkaew-Backend

A Backend service for BANGKAEW made up of FastAPI and Selenium on Docker

## Authors

- [@T-Pakorn](https://github.com/T-Pakorn)
- [@Kenta420](https://github.com/Poomipat-Ch)
- [@poomza5678](https://github.com/GoldF15h)

## Run Locally

Clone the project

```bash
  git clone https://github.com/TOC-WebScrape/bangkaew-backend.git
```

Go to the project directory

```bash
  cd bangkaew-backend
```

Start all container

```bash
  docker-compose up --build --force-recreate
```

Stop all container

```bash
  docker-compose down
```

Prune all images

```bash
  docker system prune -a
```

Get inside container

```bash
  docker-compose exec -it $(service name) bash
```

## Container Specification

| Container Name      | Port        |    Network    | Description                                                            |
| :------------------ | :---------- | :-----------: | ---------------------------------------------------------------------- |
| `selenium_services` | `-`         | `selenium_nw` | Automates browsers                                                     |
| `fast_api_service`  | `5000:5000` |   `backend`   | **Required selenium_services**. Web framework for building APIs        |
| `scrape_service`    | `5050:5050` | `selenium_nw` | **Required selenium_services**. Web scraping service that use selenium |
