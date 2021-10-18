FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# ARG PIP_EXTRA_INDEX_URL
ENV http_proxy='http://proxy.aeroport.tns:3128'
ENV https_proxy='http://proxy.aeroport.tns:3128'

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app