docker-compose rm -f corona_frontend
docker-compose build corona-frontend && docker-compose up -d corona-frontend && docker-compose logs -f