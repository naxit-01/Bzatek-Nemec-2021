# Tornado reverse-proxy router with example UI and API servers + simple cookie authentication

This repository is part of a school project. It works on its own, but provides only simple example servers to demonstrate functionality. Complete project is supposed to be a school information system. We focused on the router/reverse-proxy part, that functions as the only public access point and communicates with other servers through hidden IP addresses (keycloak is also public, since it is outsourced).

The complete project can be found here: https://github.com/hrbolek/_uois

The project is encapsulated into docker containers, as per the task assignment. However, if slighly altered, can function without containerization.

The code may contain some leftover native words from our mother language. Sorry for that :). But hey, not many of them and you should still be able to understand what it does.

## Router (tornRouter folder)

Our main part of the project. It uses python/tornado module, tornroutes: https://github.com/nod/tornroutes + some common dependancies.

It contains three main routes:

1. UI: GETs to the main graphical page, that renders html. The UI server is supposed to contain a GET to an API data server.
2. API: Returnes data, based on URI or specified GET parameters.
3. Admin: Enables to configure IP addresses and ports. For this purpose, a local sqlite database is used (more in the usage guide section).

## UI (ui_server folder)

Also written in python/tornado. Python is used to generate usable html file, which also contains javascript. This way, a request to API can be performed on the front end. I (writing this paragraph) have made the html/javascript part and am not proud of it. It is not my strong side and you are adviced against using this disgusting solution.

## API (APIs folder)

Written in python/fastapi for a change. Returns only testing data, is not connected to any database. It also handles authorization, through cookies. For instance, student can not access data about teachers or only admin can reset the server (more in the usage guide).

## Authentication (keycloak folder)

Is not an actual keycloak! Some other team had this task assigned. We named it, because it is expected to connect to customly configured keycloak container. Code only lets you log in with privileges (student, teacher, admin) without any registration or password. It then redirects back and returnes a secure cookie.

## Usage guide

At least a simple version of it!

Start the containers by running runCompose.bat. You can then navigate to http://127.0.0.1:9999, which would be the default page of the beforementioned information system. If you do not have identity cookie, you will be redirected to set them, and then back.

Without URI parameters, you are send to your personal page (/student/3 - if you login as a student with id number 3). You can require different data by changing the URI. Implemented is student, teacher, admin (below) and rozvrh (= time table :) in english).

To configure IP addresses and/or ports to non-router servers, log in as an admin and navigate to http://127.0.0.1:9999/admin. This page is very colorful and intuitive.

If you want to get rid of docker, and I understand why you would, delete all Dockerfiles, docker-compose.yml and runCompose.bat. You will need to check at what IP addresses and ports the servers run, possibly alter it, and change the paths in database (manually or through admin page). API might be a problem, the uvicorn app, it uses, is configured in its Dockerfile, so you will need to move the configuration elsewhere (into FAPI.py or custom app file).

Originally, the API server could be reset at different IP address and/or port easily. You probably do not want to do this inside docker (does not currently work, with configuration in Dockerfile), but could in the open world. You would send a request to API server, while logged in as an admin, with the new address. It would be saved into settings.txt file and reset, taking info from settings before starting uvicorn. Obviously, you have to read the txt file before running uvicorn and make use of the data (we previously did it all under __name__ == "__main__") in FAPI.py.
