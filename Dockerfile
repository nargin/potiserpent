FROM python:latest

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y
RUN apt-get install vim -y

RUN pip install --no-cache-dir -r requirements.txt

CMD ["prisma", "generate"]
CMD ["prisma", "db", "push"]

CMD ["python", "-u", "start.py"]