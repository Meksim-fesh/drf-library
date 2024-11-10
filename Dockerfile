FROM python:3.12.3-alpine3.20
LABEL maintainer="maksimnimitch@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser \
        --disabled-password \
        --no-create-home \
        my_user

USER my_user
