FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /MediaScanner
WORKDIR /MediaScanner
ADD . /MediaScanner

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
