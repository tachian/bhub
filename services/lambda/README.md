# Bhuh - Lambda

## Application that create and arrange processes

[AWS LAmbda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)

### Depencies
+ [MongoDb](https://www.mongodb.com/try/download/community) 
+ [Redis]
```
docker network create redis
docker run -d -p 6379:6379 --restart always --net redis --name "redis" redis:alpine
docker run --rm --name redis-comander -d --env REDIS_HOSTS-local:redis:6379 -p 8081:8081 --net "redis"rediscomamander/redis-commander:latest
```
