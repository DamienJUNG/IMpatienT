FROM python:3.12-bullseye

ADD ./ impatient

WORKDIR /impatient
RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get install -y libcairo2 libgl1-mesa-glx \
    && apt-get clean \
    && pip cache purge

EXPOSE 8050
CMD [ "gunicorn", "--workers=5", "--threads=1","-b 0.0.0.0:8050", "app:server"]