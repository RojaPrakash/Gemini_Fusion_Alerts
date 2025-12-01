FROM python:3.10-slim

# ------------------------------------------------------
# 1️⃣ Install system packages required for OpenCV + image processing
# ------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
 && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------
# 2️⃣ Set working directory
# ------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------
# 3️⃣ Install required Python packages
# ------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------
# 4️⃣ Copy application code
# ------------------------------------------------------
COPY . .

# ------------------------------------------------------
# 5️⃣ Expose port for Uvicorn
# ------------------------------------------------------
EXPOSE 8000

# ------------------------------------------------------
# 6️⃣ Start server
# ------------------------------------------------------
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
