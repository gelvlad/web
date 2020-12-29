FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /web
COPY . /web/
RUN pip install -r requirements.txt
