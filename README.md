# Conference Web Management System


## Setup

Follow the below steps to setup and have the docker container running:

1. Make sure Docker is installed.
2. Clone the repo
```bash
git clone <repo_link>
cd conf-wms
```
3. Build the image and make the container online.
```bash
docker build -t <image_name> .
docker run -p 8002:8000 --env-file .env -v $(pwd):/usr/src/app --name <container_name> <image_name>
```
4. The FastAPI documentation is accessible at:
   1. [Swagger UI](http://localhost:8002/docs)
   2. [Alternative UI](http://localhost:8002/redoc)

## Logs

The logs can be viewed by running:
```bash
docker logs <container_name> -f 
```

## Testing
The tests can be run by running:
```bash
docker exec <container_name> pytest
```