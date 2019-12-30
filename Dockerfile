FROM python:3.7.3-alpine3.10


WORKDIR  /usr/app

COPY .  .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["app.py"] 
