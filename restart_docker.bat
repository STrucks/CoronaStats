docker rm -f corona_frontend
docker rm -f corona_backend
docker-compose build && docker-compose up -d  && docker-compose logs -f