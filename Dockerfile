FROM python:3.9-alpine3.13

WORKDIR /application

RUN apk add --no-cache build-base python3-dev libffi-dev make musl-dev

# Install dependencies
COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

# Copy code in
COPY main.py .
COPY src     ./src

ENTRYPOINT ["python3", "/application/main.py"]
