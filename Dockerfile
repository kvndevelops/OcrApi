# Python and Linux Version 
FROM python:3.10.2-slim-buster

# COPY requirements.txt /app/requirements.txt

# Configure server
RUN apt-get update
RUN apt-get install tesseract-ocr -y
RUN apt-get update
# Install dependencies for open cv
RUN apt-get install ffmpeg libsm6 libxext6  -y
# RUN apk add tesseract-ocr
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt

# Configure server
RUN set -ex \
    && pip install --upgrade pip \  
    && pip install --no-cache-dir -r /app/requirements.txt

# Working directory
WORKDIR /app

ADD . .

# uncomment "EXPOSE 8000" when testing image locally, then re-comment before deployment! 
# EXPOSE 8000

# Line below is for testing docker image when running locally!
# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "core.wsgi:application"]

# Line below is for testing docker image when running on production - DEPLOYMENT!
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT