# pull base image
FROM python:3.10.0rc1-slim

# set python specific environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory
WORKDIR /app

# install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

# copy project
COPY ./ ./