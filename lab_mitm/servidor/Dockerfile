FROM python:3.12-slim
RUN pip install --no-cache-dir flask
WORKDIR /app
COPY app.py start.sh ./
RUN openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout key.pem -out cert.pem -days 365 -subj "/CN=servidor-web"
RUN chmod +x start.sh
EXPOSE 80 443
CMD ["./start.sh"]