FROM python:3.8.1-alpine

RUN mkdir -p /web

ENV APP_DIR = /web/shtatka
# set working directory
WORKDIR ${APP_DIR}

RUN mkdir -p  ${APP_DIR}/staticfiles
RUN mkdir -p ${APP_DIR}/media


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql

# install python dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN apk add zlib zlib-dev jpeg-dev

RUN pip install --upgrade pip

COPY ./requirements.txt ${APP_DIR}/requirements.txt

RUN pip install -r requirements.txt
COPY entrypoint.sh ${APP_DIR}/entrypoint.sh

RUN addgroup -S user && adduser -S user -G user

COPY . ${APP_DIR}
RUN chown -R user:user $APP_DIR
RUN chmod +x /home/user/web/entrypoint.sh

USER user
ENTRYPOINT ["/home/user/web/entrypoint.sh" ]

