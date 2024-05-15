.PHONY: docker-up

docker-up:
	cd deployment/docker && docker-compose up -d --build
