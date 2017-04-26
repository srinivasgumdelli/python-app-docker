FROM python:2.7-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD cd src/ && gunicorn --access-logfile /var/log/app.log --keyfile /code/localhost.key --certfile /code/localhost.crt -b 0.0.0.0:5000 main:api
