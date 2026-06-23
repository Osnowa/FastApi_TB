run-api:
	uvicorn app.main:app --reload

run-bot:
	python -m bot.main

run_redis_container:
	docker compose up -d

test:
	pytest --cov=app