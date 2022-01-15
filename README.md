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

Časový harmonogram:

    5.11. UI admin
    12.11 api server
    19. 11. UI(Client) server
    26.11. Cookies(komunikace s Keycloak)
    3.12 baleni do Dockeru
    10.12 dokumentace
    15.12 odevzdavani alfa verze
    16.12-15.1. prace na Beta verzi (podle vysledku alfa verze)
    15.1. odevzdani beta verze
    16.1.-23.1. dokonceni projektu
    24.1. odevzdavani hotoveho projektu a obhajoba









    1. 11. 2021 zveřejnění harmonogramu prací na projektu,
    1. 11. 2021 zveřejnění identifikovaných nejsložitějších problémů v projektu,
    15. 12. 2021 verze Alfa,
    15. 1. 2022 verze Beta,
    24. 1. 2021 počátek zkouškového období,
    31. 1. 2022 uzavření projektu,
    18. 3. 2022 konec zkouškového období. 
