FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DEBUG=0

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]