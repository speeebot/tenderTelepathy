FROM python:3
FROM gorialis/discord.py

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/telepathy
RUN  python -m pip install 'pymongo[srv]'
RUN  python3 -m pip install python-dotenv

WORKDIR /usr/src/telepathy

COPY . .

CMD [ "python3", "-u", "telepathy.py" ]