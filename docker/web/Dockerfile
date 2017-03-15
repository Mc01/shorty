FROM python:3.6
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip freeze
ADD . /app
WORKDIR /app
COPY docker/web/run.sh run.sh
