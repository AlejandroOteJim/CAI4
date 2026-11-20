FROM debian:stable-slim
RUN apt-get update && apt-get install -y curl iproute2 iputils-ping \
    && rm -rf /var/lib/apt/lists/*
CMD ["sleep", "infinity"]