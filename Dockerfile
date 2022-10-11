FROM python:3.9

ENV CONTAINER_HOME=/var/www

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN pip install -r $CONTAINER_HOME/requirements.txt
RUN pip install mysql-connector-python pandas -U flask-cors flask-mysql requests numpy