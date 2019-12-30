## Environment Variables

- REDIS_HOST
  
  - Redis host details / ip or service name.

- REDIS_PORT 

  - Default : 6379 
  - Portnumber of the redis port.

- REDIS_CACHE
  - Default : 300
  - Time to specify how long the redis should maintain the cached records.


- FLASK_PORT
  - Default : 8080
  - Default port number of the flask server.

- IPSTACK_KEY
  - ipstack api token.


 

## Example

#### Creating bridge network.
```

docker network create --driver bridge appnet
```


#### Creating redis container.

```
docker run \
-d \
--name redis \
--network appnet \
--restart always \
redis:latest
```

#### Creating ipstackapp container.

```
docker run \
-d \
--name ipstackapp \
--network appnet \
--restart always \
-p 80:8080 \
-e REDIS_HOST=redis \
-e REDIS_CACHE=300 \
-e FLASK_PORT=8080 \
-e IPSTACK_KEY='0454ac34a0a6697c43af345b393360f5' \
fujikomalan/ipstackapp:1

```
