FROM python:3.8

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

RUN flask run