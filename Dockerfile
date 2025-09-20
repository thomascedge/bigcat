FROM python:3.10-slim

LABEL maintainer="thomas@thomascedge.com"

# unbuffered env variables
ENV PYTHONUNBUFFERED 1

WORKDIR /src

# copy requirements file over
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application to container
COPY . /src 

# FastAPI port
EXPOSE 8000

# Healthcheck to monitor the application
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

# run the application
CMD ["uvicorn", "main:src", "--host", "0.0.0.0", "--port", "8000"]
