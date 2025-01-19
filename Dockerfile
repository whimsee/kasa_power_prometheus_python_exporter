FROM python:3.11.11-bookworm
WORKDIR /usr/local/app

COPY requirements.txt ./
COPY exporter.py ./
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 10240

RUN useradd app
USER app

CMD ["python3", "exporter.py"]
