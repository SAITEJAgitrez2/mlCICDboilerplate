FROM python:3.8-slim-buster

# Install necessary system dependencies
RUN apt update -y && apt install -y \
    awscli \
    gcc \
    libzstd-dev \
    python3-dev \
    build-essential

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip  # Upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade accelerate
RUN pip uninstall -y transformers accelerate
RUN pip install transformers accelerate

CMD ["python3", "app.py"]
