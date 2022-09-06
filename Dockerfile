FROM python:3.8.1-alpine

ENV PYHTONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# creating a folder.
RUN mkdir -p /web/shtatka

ENV APP_HOME=/web

WORKDIR ${APP_HOME}

RUN mkdir ${APP_HOME}/staticfiles
RUN mkdir ${APP_HOME}/media


RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN apk add zlib zlib-dev jpeg-dev

RUN pip install --upgrade pip

COPY ./requirements.txt ${APP_HOME}/requirements.txt

RUN apk add build-base
RUN pip install -r requirements.txt
COPY entrypoint.sh ${APP_HOME}/entrypoint.sh

RUN addgroup -S user && adduser -S user -G user

COPY . ${APP_HOME}
RUN chown -R user:user $APP_HOME
RUN chmod +x /web/shtatka/entrypoint.sh

USER user
ENTRYPOINT ["/web/shtatka/entrypoint.sh" ]

