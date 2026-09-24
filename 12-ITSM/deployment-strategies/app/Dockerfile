FROM python:3.11-slim

ARG VERSION=v1
ARG COLOR="#2196F3"
ARG APP_NAME="Sample App"

ENV APP_VERSION=${VERSION}
ENV APP_COLOR=${COLOR}
ENV APP_NAME=${APP_NAME}

WORKDIR /app
COPY app.py .
COPY templates/ templates/

RUN pip install flask --no-cache-dir

EXPOSE 8080
CMD ["python", "app.py"]
