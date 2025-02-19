FROM python:3.9-alpine

WORKDIR /app
COPY app.py ./
COPY requirements.txt ./
COPY static static
COPY templates templates
RUN chmod -R 775 . && \
    chmod 1773 static/feedbacks templates/errors

RUN pip install -r requirements.txt

RUN adduser -D user
USER user

CMD python app.py
