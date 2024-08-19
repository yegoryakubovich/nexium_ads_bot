FROM python:3.11-slim

WORKDIR /app/src/bot
COPY src/bot /app/src/bot
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]