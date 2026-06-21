run:
	uvicorn app.main:app --reload

test:
	pytest --cov=app