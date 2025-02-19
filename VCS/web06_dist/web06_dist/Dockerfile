FROM python:3.9-alpine
RUN apk add --no-cache chromium chromium-chromedriver
COPY  ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./start.sh /start.sh
COPY ./src /app
COPY ./bot /bot
CMD [ "/bin/sh", "/start.sh" ]
