FROM python:3

RUN mkdir wd

COPY requirements.txt ./wd
WORKDIR /wd
RUN pip install -r requirements.txt

COPY ../ ./
# CMD python3 app.py
EXPOSE 8050
CMD [ "gunicorn", "--workers=5", "--threads=1","-b 0.0.0.0:8050", "app:server"]