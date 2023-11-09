FROM python:3.10.5

WORKDIR /app

COPY app /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]