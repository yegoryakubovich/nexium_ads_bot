FROM python:3.11-slim

WORKDIR /app/src/userbot
COPY src/userbot /app/src/userbot
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
