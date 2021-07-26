FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY backend /usr/src/app

EXPOSE 5010

ENTRYPOINT ["python3"]

CMD ["-m", "com.strucks.coronastats"]