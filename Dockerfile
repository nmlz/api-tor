FROM python:3.8

WORKDIR /api

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY /app.py /app.py

CMD ["python", "/app.py"]