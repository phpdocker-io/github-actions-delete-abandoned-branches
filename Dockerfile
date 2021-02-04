FROM python:3.9-alpine

WORKDIR /application

# Install dependencies
COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

# Copy code in
COPY main.py .
COPY src     ./src

ENTRYPOINT ["python3", "/application/main.py"]
