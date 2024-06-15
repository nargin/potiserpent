up:
	docker-compose up -d

b:
	docker-compose up -d --build

bl:
	docker-compose up -d --build
	docker logs -f bot

down:
	docker-compose down

fclean:
	docker-compose down
	docker system prune -f