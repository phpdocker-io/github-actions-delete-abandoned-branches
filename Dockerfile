FROM python:3.9-alpine

WORKDIR /application

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

# Install dependencies
COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

# Copy code in
COPY main.py .
COPY src     ./src

ENTRYPOINT ["python3", "/application/main.py"]
