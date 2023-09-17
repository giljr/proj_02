## Compose sample application

### Use with Docker Development Environments

You can open this sample in the Dev Environments feature of Docker Desktop version 4.12 or later.

[Open in Docker Dev Environments <img src="../open_in_new.svg" alt="Open in Docker Dev Environments" align="top"/>](https://open.docker.com/dashboard/dev-envs?url=https://github.com/docker/awesome-compose/tree/master/nginx-flask-mysql)

### Python/Flask with Nginx proxy and MySQL database

Project structure:
```
.
├── compose.yaml
├── flask
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
└── nginx
    └── nginx.conf

```

[_compose.yaml_](compose.yaml)
```
services:
  backend:
    build:
      context: backend
      target: builder
    ...
  db:
    # We use a mariadb image which supports both amd64 & arm64 architecture
    image: mariadb:10-focal
    # If you really want to use MySQL, uncomment the following line
    #image: mysql:8
    ...
  proxy:
    build: proxy
    ...
```
The compose file defines an application with three services `proxy`, `backend` and `db`.
When deploying the application, docker compose maps port 80 of the proxy service container to port 80 of the host as specified in the file.
Make sure port 80 on the host is not already being in use.

> ℹ️ **_INFO_**  
> For compatibility purpose between `AMD64` and `ARM64` architecture, we use a MariaDB as database instead of MySQL.  
> You still can use the MySQL image by uncommenting the following line in the Compose file   
> `#image: mysql:8`

## Deploy with docker compose

```
$ docker compose up -d
$ docker-compose up -d
Creating network "proj_02_backnet" with the default driver
Creating network "proj_02_frontnet" with the default driver
Creating volume "proj_02_db-data" with default driver
Pulling db (mariadb:10-focal)...
10-focal: Pulling from library/mariadb
...
WARNING: Image for service backend was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Building proxy
[+] Building 2.7s (7/7) FINISHED                                                                                                        docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                    0.0s
 => => transferring dockerfile: 100B                                                                                                                    0.0s
 ...

What's Next?
  View summary of image vulnerabilities and recommendations → docker scout quickview
WARNING: Image for service proxy was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Creating proj_02_db_1 ... done
Creating proj_02_backend_1 ... done
Creating proj_02_proxy_1   ... done
```

## Expected result

Listing containers should show three containers running and the port mapping as below:
```
$ docker compose ps
NAME                IMAGE               COMMAND                  SERVICE             CREATED             STATUS                   PORTS
proj_02_backend_1   proj_02_backend     "flask run"              backend             8 minutes ago       Up 8 minutes             0.0.0.0:8000->8000/tcp
proj_02_db_1        mariadb:10-focal    "docker-entrypoint.s…"   db                  8 minutes ago       Up 8 minutes (healthy)   3306/tcp, 33060/tcp
proj_02_proxy_1     proj_02_proxy       "nginx -g 'daemon of…"   proxy               8 minutes ago       Up 8 minutes             0.0.0.0:80->80/tcp
```

After the application starts, navigate to `http://localhost:80` in your web browser or run:
```
$ curl localhost:80
[{"id": 1, "code": 65014, "date": "2019-01-12", "store": "Shopping Morumbi", "product": "Aster Pants", "qty": 5, "price": 114}, {"id": 2, "code": 65014, "date": "2019-01-12", "store": "Shopping Morumbi", "product": "Trench Coat", "qty": 1, "price": 269}, {"id": 3, "code": 65016, "date": "2019-01-12", "store": "Iguatemi Campinas", "product": "Peter Pan Collar", "qty": 3, "price": 363}]
```

Stop and remove the containers
```
$ docker compose down
```
