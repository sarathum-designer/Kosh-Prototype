FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY . .
WORKDIR /app/backend
ENV PORT=8080 KOSH_DB=/data/kosh.db
RUN mkdir -p /data
EXPOSE 8080
CMD ["python", "-m", "kosh.app"]
