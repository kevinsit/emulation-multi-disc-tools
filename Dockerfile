FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    mame-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data

COPY convert.sh /usr/local/bin/convert.sh
RUN chmod +x /usr/local/bin/convert.sh

ENTRYPOINT ["/usr/local/bin/convert.sh"]
