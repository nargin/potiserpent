FROM python:latest

WORKDIR /app

COPY . .

COPY .env .env

RUN apt-get update && apt-get install -y
RUN apt-get install vim -y

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "start.py"]