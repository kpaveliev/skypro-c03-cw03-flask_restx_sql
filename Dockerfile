FROM python:3.10-slim

# set work directory
WORKDIR /code

# set environment variables
ENV FLASK_APP=run.py

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY run.py run.py
COPY project project
COPY data_scripts data_scripts
COPY migrations migrations
COPY docker_config.py default_config.py

# run flask
CMD flask run -h 0.0.0.0 -p 80