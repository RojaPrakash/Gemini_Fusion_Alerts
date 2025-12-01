FROM python:3.10

WORKDIR /app

RUN pip install --no-cache-dir opencv-python-headless numpy requests

COPY . /app

CMD ["python", "cctv_fetcher.py"]
