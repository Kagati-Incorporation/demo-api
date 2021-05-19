FROM python:3.8
LABEL maintainer="Kagati <techkagati@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /demo
RUN mkdir /demo/static
RUN mkdir /demo/media
# RUN apk update and apk add build-essential postgresql-dev gcc python3-dev musl-dev libzbar-dev linux-headers
COPY requirements.txt /demo/
RUN apt-get update \
  && apt-get install -y build-essential curl libpq-dev --no-install-recommends
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /demo/