FROM python:3.10

WORKDIR /server-chatbot

COPY requirements.txt .
COPY ./src ./src

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]