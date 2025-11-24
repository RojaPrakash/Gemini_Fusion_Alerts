FROM python:3.10

WORKDIR /app

# Install OpenCV and dependencies
RUN pip install --no-cache-dir opencv-python-headless numpy requests

# Copy your fetcher code
COPY . /app

# Default command
CMD ["python", "cctv_fetcher.py"]
