FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app
RUN apk add build-base
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip 
RUN pip install Django==4.1.4 neo4j python-dotenv djangorestframework 

# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]