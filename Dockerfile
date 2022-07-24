FROM python:3

ENV PYTHONNUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install flask
RUN pip install "pymongo[srv]"
RUN pip install flask-dotenv
RUN pip install flask_dotenv
RUN pip install flask_pymongo
RUN pip install flask-wtf
RUN pip install dnspython
RUN pip install gunicorn

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app