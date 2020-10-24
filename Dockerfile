# Initially built as docker image pingue/grava-backend
# Example usage: 
# docker run --rm -e GRAVA_INFLUX_HOST=influx -v /path/to/authfiles:/grava/authfiles pingue/grava-backend

FROM python:3.6-stretch

COPY . /grava

RUN pip install -r /grava/requirements.txt

WORKDIR /grava

CMD python3 /grava/grava_init_backend.py
