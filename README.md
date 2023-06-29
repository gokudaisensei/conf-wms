# Conference Web Management System

## Setup

Follow the below steps to setup and have the multi-part docker container running:

1. Make sure Docker is installed.
2. Clone the repo
```bash
git clone <repo_link>
cd conf-wms
```
3. Build the image and make the container online.
```bash
docker-compose up -d --build
```
4. The FastAPI documentation is accessible at:
   1. [Swagger UI](http://localhost:8002/docs)
   2. [Alternative UI](http://localhost:8002/redoc)

## Logs

The logs can be viewed by running:
```bash
docker-compose logs -f <service_name>
```

## Testing
The tests can be run by running:
```bash
docker-compose exec web bash
pytest
```
This is for running the tests written for FastAPI. For accessing MySQL:
```bash
docker-compose exec db bash
mysql -uroot -proot
```
