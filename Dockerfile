FROM python:3

RUN mkdir wd

COPY requirements.txt ./wd
WORKDIR /wd
RUN pip3 install -r requirements.txt

COPY ../ ./
# CMD python3 app.py
EXPOSE 8050
CMD [ "gunicorn", "--workers=5", "--threads=1", "app:server"]