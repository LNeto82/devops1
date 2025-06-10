FROM python:3.9

WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 3002

CMD ["python", "app.py"]
