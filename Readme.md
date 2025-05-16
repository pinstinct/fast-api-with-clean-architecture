## 데이터베이스 설정

```shell
docker exec -it <container-id> bash
mysql -u root -h 127.0.0.1 -p
mysql> SHOW DATABASES;
mysql> CREATE SCHEMA `fastapi-ca;
```