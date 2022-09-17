FROM nginx:1.17.9-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir -p /etc/nginx/certs/
COPY fastapicode_com.crt /etc/nginx/certs/fastapicode_com.crt
COPY fastapicode_com.key /etc/nginx/certs/fastapicode_com.key
