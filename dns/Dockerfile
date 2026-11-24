FROM alpine
RUN apk add --no-cache dnsmasq
CMD ["dnsmasq", "-k", "--no-resolv", "--address=/hospital.lab/172.20.0.10", "--log-queries"]
