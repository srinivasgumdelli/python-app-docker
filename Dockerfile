FROM python:2.7-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["gunicorn", "main:api", "-b", "0.0.0.0:8000"]
