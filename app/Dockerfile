FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update -q \
    && apt-get upgrade -qy \
    && apt-get install -y \
        gettext \
        vim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip3 install pip --upgrade --force-reinstall \
    && pip3 install -r /app/requirements.txt
ADD . /app/
# this must be used for dev envs with nginx container
CMD ["python3", "/app/manage.py", "runserver", "0:8888"]

# the following only works on prod env
# keep it on one line, Dockerfile does not support multiline commands
# `uwsgi` must be installed via pip
#CMD ["uwsgi", "--http", "0.0.0.0:8888", "--chdir", "/app", "--wsgi-file", "/app/teleautobot/wsgi.py", "--callable", "application", "--processes", "2", "--threads", "4" ]
# using ini file does not work for an unknown reason
