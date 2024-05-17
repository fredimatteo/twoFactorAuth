.PHONY: docker-up

docker-up:
	cd deployment/docker && docker-compose up -d

docker-build-up:
	cd deployment/docker && docker-compose up -d --build

docker-down:
	cd deployment/docker && docker-compose down

docker-down-v:
	cd deployment/docker && docker-compose down -v
