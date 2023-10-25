# docker build -t lambda-sample .
FROM --platform=linux/amd64 python:3.11-slim

# Install dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./app/ /var/www/app/
COPY ./notion_client_wrapper/ /var/www/notion_client_wrapper/

WORKDIR /var/www

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
