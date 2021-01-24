FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
ENV BUCKET=bucket

CMD ["python", "/app/estrazione.py"]                    
