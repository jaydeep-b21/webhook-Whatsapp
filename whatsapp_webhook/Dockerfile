# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb-dev-compat \
    libssl-dev \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Copy dependencies and application code
COPY requirements.txt .
#RUN pip install  pywin32
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install  django
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the Django application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
