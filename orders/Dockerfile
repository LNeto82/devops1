FROM python:3.9

WORKDIR /app

COPY app.py .

RUN pip install flask redis mysql-connector-python requests

EXPOSE 4002

CMD ["python", "app.py"]
