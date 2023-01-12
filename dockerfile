FROM python:3.10

WORKDIR /app

RUN apt update && apt install netcat postgresql-client dnsutils -y

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${PORT}

COPY ./entrypoint.sh /app/

RUN ["chmod", "+x", "/app/entrypoint.sh"]
ENTRYPOINT ["/app/entrypoint.sh"]

CMD gunicorn -w 1 -b 0.0.0.0:${PORT} -k uvicorn.workers.UvicornWorker -t 1200 --threads 4 main:app