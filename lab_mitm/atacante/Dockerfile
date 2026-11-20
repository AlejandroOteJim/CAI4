FROM debian:stable-slim
RUN apt-get update && apt-get install -y bettercap iproute2 iptables \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /caplets
COPY caplets/ /caplets/
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]