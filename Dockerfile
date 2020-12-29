FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /web
COPY . /web/
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
