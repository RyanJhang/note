
```
docker build -t my_flask_docker . --no-cache

docker run -d -p 5000:5000 --name my_flask_docker my_flask_docker:latest

docker port my_flask_docker

curl http://localhost:5000
```