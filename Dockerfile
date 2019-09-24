FROM python:3-alpine

ENV DEVELOPER="Diego Quan"
ENV APP_HOME=/
WORKDIR ${APP_HOME}
ADD . /app

RUN pip install -r requirements.txt

CMD ["./soup.py"]
ENTRYPOINT [ "python" ]