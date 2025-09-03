# build stage
FROM python:2.12-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cahce-dir -r requirements.txt

# copy project files
COPY src/ src/

# expose the port FastAPI runs on
EXPOSE 8000

# run application
CMD ['uvicorn', 'src.main:app', '--host', '0.0.0.0', '--port', '8000']
