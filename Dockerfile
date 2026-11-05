FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home appuser

COPY dekoder.py web.py koder.py morse.xsd ./
COPY templates/ ./templates/
USER appuser
EXPOSE 8000
CMD ["python", "web.py"]