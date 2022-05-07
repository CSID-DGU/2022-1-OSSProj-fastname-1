FROM tiangolo/uwsgi-nginx-flask:python3.8

FROM node:6.2.2
##

COPY ./app /app
