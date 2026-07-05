run-api:
	uvicorn app.main:app --reload

run-bot:
	watchmedo auto-restart \
    --directory=. \
    --pattern=*.py \
    --recursive \
    -- python -m bot.main

run_redis_container:
	docker compose up -d

test:
	pytest --cov=app