FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    PORT=3000

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY manus-routes.json .
EXPOSE 3000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-3000} --workers 2 --timeout 120 app:app"]
