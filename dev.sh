#!/bin/bash

# Check sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi


clear
ROOTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m'


# MySQL defaults
export MYSQL_HOST=${MYSQL_HOST:-'cve-mysql'}
export MYSQL_PORT=${MYSQL_PORT:-3306}
export MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD:-$(openssl rand -hex 16)}
export MYSQL_DB=${MYSQL_DB:-'cvedb'}
export MYSQL_USER=${MYSQL_USER:-'cveuser'}
export MYSQL_PASSWD=${MYSQL_PASSWD:-$(openssl rand -hex 16)}

# App defaults
export BACKEND_URL='http://localhost:8002'
export SECRET=${SECRET:-$(openssl rand -hex 32)}


# Save variables to .env file
echo "MYSQL_HOST=$MYSQL_HOST" > .env
echo "MYSQL_PORT=$MYSQL_PORT" >> .env
echo "MYSQL_DB=$MYSQL_DB" >> .env
echo "MYSQL_USER=$MYSQL_USER" >> .env
echo "MYSQL_PASSWD=$MYSQL_PASSWD" >> .env
echo "MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD" >> .env
echo "SECRET=$SECRET" >> .env

if [[ "$@" == *"--restart"* ]]; then
    # Restart containers
    printf "\n\n${GREEN}Restarting environment${NC}\n"
    docker compose -f "$ROOTDIR/docker-compose-dev.yml" restart
elif [[ "$@" == *"--stop"* ]]; then
    # Stoping containers
    printf "\n\n${RED}Stopping environment${NC}\n"
    docker compose -f "$ROOTDIR/docker-compose-dev.yml" stop
    exit 1
else
    # Stop and remove containers, networks
    printf "\n\n${RED}Removing old containers${NC}\n"
    docker compose -f "$ROOTDIR/docker-compose-dev.yml" down

    # Create Docker network if it doesn't exist
    docker network inspect cve-network >/dev/null 2>&1 || \
    docker network create cve-network

    # Run
    printf "\n\n${GREEN}Starting environment${NC}\n"
    docker compose -f "$ROOTDIR/docker-compose-dev.yml" up -d
fi


# Print variables
printf "\n\n${PURPLE}Environment variables:${NC}\n"
printf "MYSQL_ROOT_PASSWORD: $MYSQL_ROOT_PASSWORD\n"
printf "MYSQL_DB: $MYSQL_DB\n"
printf "MYSQL_HOST: $MYSQL_HOST\n"
printf "MYSQL_PASSWD: $MYSQL_PASSWD\n"
printf "MYSQL_PORT: $MYSQL_PORT\n"
printf "MYSQL_USER: $MYSQL_USER\n"
printf "SECRET: $SECRET\n"
printf "${RED}Credential are stored in .env${NC}\n"


# Creating .env for vue
echo "BACKEND_URL=$BACKEND_URL" > frontend/.env

printf "\n\n${PURPLE}Containers:${NC}\n"
docker ps

printf "\n\n${PURPLE}Servers:${NC}\n"
printf "Frontend: http://localhost:8001\n"
printf "Backend: ${BACKEND_URL}\n\n"

printf "\n\n${PURPLE}Logs:${NC}\n"
docker compose -f "$ROOTDIR/docker-compose-dev.yml" logs --follow