FROM python:3

ENV PYTHONNUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip3 install flask
RUN pip3 install "pymongo[srv]"
RUN pip3 install Flask-Pymongo
RUN pip3 install flask_pymongo
RUN pip3 install flask-pymongo
RUN pip3 install flask-wtf
RUN pip3 install dnspython
RUN pip3 install gunicorn

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app