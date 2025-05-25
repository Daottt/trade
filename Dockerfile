
FROM python:3.10.17-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

ENV DJANGO_SUPERUSER_EMAIL="admin@main.com"
ENV DJANGO_SUPERUSER_USERNAME="admin"
ENV DJANGO_SUPERUSER_PASSWORD="admin"

ENTRYPOINT bash -c "python manage.py migrate --noinput && \
                    python manage.py initadmin && \
                    python manage.py runserver 0.0.0.0:8000"
