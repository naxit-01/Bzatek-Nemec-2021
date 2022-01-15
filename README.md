# Tornado router with example UI and API + simple cookie authentication

This is a part of a school project. It works on its own, but provides only simple example servers to demonstrate functionality. Complete project is supposed to be a school information system. We focused on the router part, that functions as the only public access point and comunicates with other servers with hidden IPs (keycloak is also public, since it is outsourced).

The complete project can be found here: https://github.com/hrbolek/_uois

The project is encaplulated into docker container, as per the task assignment. However, if slighly altered, can function without containerization.

The code may contain some leftover native words from our mother language. Sorry for that :). But hey, not many of them and you should still be able to understand what it does.

## Router (tornRouter folder)

Our main part of the project. It uses python/tornado module, tornroutes: https://github.com/nod/tornroutes + some common dependancies.

It contains three main routes:

1. UI: Redirects to the main graphical page, that renders html. The UI server is supposed to contain a GET to API data server.\
2. API: Returnes data based on URI or specified GET parameters.\
3. Admin: Enables to configure IP addresses and ports. For this purpose, a local sqlite database can be configured at http://localhost:9999/admin

## UI (ui_server folder)

Also written in python/tornado. Python is used to generate usable html file, which also contains javascript. This way, a request to API can be performed on the front end. I (writing this paragraph) have made the html/javascript part and I am not proud of it. It is not my strong side and you are adviced ahains using this solution.

## API (APIs folder)

Written in fastapi for a change. Returns only testing data, is not connedcted to any database. It aslo handles authorization, through cookies. For instance, student can not access data about teachers.

## Authentication (keycloak folder)

Is not actual keycloak! Some other team had this task assigned. We named it, because it is expected to connect to customly configured keycloak container. Code only lets you log in with privileges (student, teacher, admin) without any registration or password. It then redirects back and returnes a secure cookie.

## Usage guide

Start the containers by running compose.bat. You can then navigate to http://127.0.0.1:9999, which would be the default page of the beforementioned information system. If you do not have identity cookie, you will be redirected to set them, and then back.

Without URI paramets, you are send to your personal page (/student/3 - if you login as student with id 3). You can require different data by changing the URI.

To configure IP addresses and/or ports to non-router servers, log in as an admin and navigate to http://127.0.0.1:9999/admin.

If you want to get rid of docked, and I understand why you would, delete all dockerfiles, docker.compose and run.bat. You will need to check at what IP addresses and ports are the servers running, alter it, if you wish, and change the paths in database (manually or through admin page). API might be a problem, the uvicorn app, it uses, is configured in dockerfile, so you need to move the configuration elsewhere (into FAPI.py or custom app file).
