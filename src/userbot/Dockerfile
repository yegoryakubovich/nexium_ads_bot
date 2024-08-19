FROM python:3.11-slim

COPY .. /app/src
RUN pip install --no-cache-dir -r /app/src/bot/requirements.txt
CMD ["python", "main.py"]
