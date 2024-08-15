FROM python:3.11-slim

RUN pip install --no-cache-dir -r requirements.txt
COPY src /app/src
CMD ["python", "main.py"]
