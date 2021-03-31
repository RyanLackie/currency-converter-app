FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /server-py
COPY requirements.txt /server-py/
RUN pip install -r requirements.txt
COPY . /server-py/