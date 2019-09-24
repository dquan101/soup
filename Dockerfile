FROM python:3-alpine

ENV DEVELOPER="Diego Quan" APP_HOME=/
WORKDIR ${APP_HOME}
ADD . /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt


ENTRYPOINT [ "python", "./soup.py" ]