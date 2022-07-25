FROM python:3

ENV PYTHONNUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

<<<<<<< HEAD
RUN pip3 install flask
RUN pip3 install "pymongo[srv]"
RUN pip3 install Flask-Pymongo
RUN pip3 install flask_pymongo
RUN pip3 install flask-pymongo
RUN pip3 install python-dotenv
RUN pip3 install flask-wtf
RUN pip3 install dnspython
RUN pip3 install gunicorn
=======
RUN pip install -r requirements.txt
RUN pip install gunicorn
>>>>>>> 34739702a3a4a10aa71ac17a077fa31b5a94cec2

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app