FROM python:3.14.0a4-slim-bookworm
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10240

RUN useradd app
USER app

CMD ["python3", "exporter.py"]
