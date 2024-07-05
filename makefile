install :
	pip install -r requirements.txt
docker-build :
	docker build -t impatient .
docker-run :
	docker run --rm -p 0.0.0.0:8050:8050 impatient
python-run :
	python3 app.py