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

| Container Name      | Exposed Port          |    Network    | Description                                                            |
| :------------------ | :-------------------- | :-----------: | ---------------------------------------------------------------------- |
| `selenium_services` | `4444:4444`           | `selenium_nw` | Automates browsers                                                     |
| `fast_api_service`  | `5000:5000`           |   `backend`   | **Required selenium_services**. Web framework for building APIs        |
| `scrape_service`    | `5050:5050`           | `selenium_nw` | **Required selenium_services**. Web scraping service that use selenium |
| `spark-master`      | `8080:8080,7077:7077` |  `spark_nw`   | Spark Master container with Spark Admin                                |
| `spark-worker`      | `-`                   |  `spark_nw`   | **Required spark-master**. Spark Worker                                |

## Spark Worker Specification

| Specification Parameter | Value |
| :---------------------- | :---- |
| `SPARK_WORKER_MEMORY`   | `1G`  |
| `SPARK_WORKER_CORES`    | `1`   |
