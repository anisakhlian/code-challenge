FROM python:3.8.10

WORKDIR /app

ENV PYTHONPATH=$PYTHONPATH:/app

USER root

RUN pip3 install pip==21.1.3
RUN pip3 install wheel==0.35.1
RUN pip3 install gunicorn==20.0.4 gevent==21.1.2

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["-w", "4"]
