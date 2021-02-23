docker-compose rm -f corona_frontend
docker-compose build && docker-compose up -d  && docker-compose logs -f