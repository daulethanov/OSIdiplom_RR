FROM python:3.11

WORKDIR /backend

COPY req.txt ./

RUN pip install -r req.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:5000 app:app


