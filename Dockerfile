FROM python:3

ADD ./ impatient

WORKDIR /impatient
RUN pip install -r requirements.txt

# CMD python3 app.py
EXPOSE 8050
CMD [ "gunicorn", "--workers=5", "--threads=1","-b 0.0.0.0:8050", "app:server"]