FROM python:3.9
COPY ./app /app
RUN pip install -r /app/requirements.txt
ENV PYTHONPATH=/MovieDatabase
WORKDIR /app