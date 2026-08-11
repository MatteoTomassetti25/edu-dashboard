FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 TZ=Europe/Rome DATA_DIR=/data
WORKDIR /srv
COPY server.py index.html ./
EXPOSE 8800
CMD ["python3", "server.py"]
