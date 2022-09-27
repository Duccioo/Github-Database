FROM arm64v8/python:3.9.14-alpine3.16

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN apk update
RUN apk upgrade
RUN apk add git
RUN apk add libffi-dev gcc libc-dev


COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app

COPY . /app

CMD [ "python", "./src/bot.py","&" ]