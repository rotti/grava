# Initially built as docker image pingue/grava-backend

FROM python:3.6-stretch

COPY . /grava

RUN pip install -r /grava/requirements.txt

CMD python3 /grava/grava_init_backend.py
