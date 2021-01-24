FROM python:3.7


RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

VOLUME /.kube/default

CMD celery -A celery worker --loglevel=info    
