FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
ENV BUCKET=bucketzf
ENV OBJECT_NAME=Compressa.zip
ENV MODEL_FILE=Compressa.zip
ENV NAME_FILE=testo.txt
ENV NAME_FILE1=model.py
ENV MODEL_DIR=/app/Compressa


CMD ["python", "/app/estrazione.py"]                    
