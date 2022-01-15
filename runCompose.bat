set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose -p proxyServer up -d --build
pause
docker-compose -p proxyServer down