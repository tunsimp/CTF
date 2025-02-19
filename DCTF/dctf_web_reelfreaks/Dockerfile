FROM python:latest

RUN apt update

RUN pip install flask Flask-SQLAlchemy flask_login werkzeug playwright cryptography
RUN playwright install-deps

RUN useradd ctf

COPY src/ /home/ctf/src
RUN chown -R ctf:ctf /home/ctf

ENV ADMIN_PASS=admin
ENV ADMIN_USER=admin

ENV FLASK_APP=src


USER ctf

RUN playwright install chromium

WORKDIR /home/ctf

EXPOSE 5000
ENTRYPOINT flask run --host="0.0.0.0" --cert=adhoc