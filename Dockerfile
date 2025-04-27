# Gunakan image Python slim sebagai dasar
FROM python:3.9-slim

# Install dependencies untuk build dlib dan face-recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory di dalam container
WORKDIR /app

# Copy semua file dari proyek ke dalam container
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies dari requirements.txt
RUN pip install -r requirements.txt

# Tentukan port yang digunakan oleh aplikasi
EXPOSE 5000

# Perintah untuk menjalankan aplikasi Flask
CMD ["python", "app.py"]
