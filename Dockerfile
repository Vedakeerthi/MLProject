FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app 

RUN pip install --no-cache-dir -r r.txt
CMD ['python3','app.py']