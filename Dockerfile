FROM python:3.12

WORKDIR /potiserpent

COPY . .

COPY .env .env

RUN apt-get update && apt-get install -y

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "src/entrypoint.py"]