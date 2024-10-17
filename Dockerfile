FROM python:3.9

# Set the working directory to /app
WORKDIR /main

# Copy the contents in requirements.txt
COPY requirements.txt .

# Install the necessary packages
RUN apt-get install -y wget curl unzip fontconfig locales \
    libxrender1 libxss1 libxtst6 libnss3 libgconf-2-4 libgbm1 \
    libasound2 libx11-xcb1 libxshmfence1

# Install the necessary packages
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /text-visionary
COPY . /main

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start the Flask app
CMD ["python", "main.py"]
