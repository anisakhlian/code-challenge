.PHONY: api
api:
	docker-compose up --build

.PHONY: app
app:
	cd ./app && \
	yarn && \
	yarn start

.PHONY: test
test:
	docker exec -it `docker container ps --filter "name=code_challenge_api" -q` python3 -m unittest
	cd ./app && yarn test --watchAll=false

.PHONY: clean
clean:
	docker rm code_challenge_api code_challenge_postgres