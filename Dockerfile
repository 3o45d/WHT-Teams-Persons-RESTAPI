FROM python:3.12
LABEL authors="coded"

WORKDIR /app


# Gеременные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Pависимости
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
COPY ./generate_secret.sh /generate_secret.sh
RUN chmod +x /generate_secret.sh && ./generate_secret.sh
