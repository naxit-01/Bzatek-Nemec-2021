# Tornado router with example UI and API + simple cookie authentication
This is a part of a school project. It works on its own, but provides only simple example servers to demonstrate functionality. Complete project is supposed to be a school information system. We focused on the router part, that functions as the only public access point and comunicates with other servers with hidden IPs (keycloak is also public, since it is outsourced).\
The complete project can be found here: <external repo, hrbolek uo_is>\
The project is encaplulated into docker container, as per the task assignment. However, if slighly altered, can function without containerization.\
The code may contain some leftover native words from our mother language. Sorry for that :). But hey, not many of them and you should still be able to understand what it does.

## Router (tornRouter folder)
Our main part of the project. It uses python/tornado module, tornroutes: <external project repo> + some common dependancies.\
It contains three main routes:\
    1. UI: Redirects to the main graphical page, that renders html. The UI server is supposed to contain a GET to API data server.\
    2. API: Returnes data based on URI or specified GET parameters.\
    3. Admin: Enables to configure IP addresses and ports. For this purpose, a local sqlite database is used.\

## UI (ui_server folder)
Also written in python/tornado. Python is used to generate usable html file, which also contains javascript. This way, a request to API can be performed on the front end. I (writing this paragraph) have made the html/javascript part and I am not proud of it. 
