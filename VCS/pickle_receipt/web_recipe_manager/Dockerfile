FROM python:3.11.1-alpine3.17

# Install packages
RUN apk add --update --no-cache supervisor 

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

# Add application
COPY challenge .
COPY flag.txt /flag.txt
RUN chmod 444 /flag.txt 
RUN python3 - <<'PY'
import os, secrets
src = "/flag.txt"
dst = f"/flag_{secrets.token_hex(6)}.txt"
os.rename(src, dst)
PY

# Copy configs
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 1337

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
