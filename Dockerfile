FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including templates and stocks.csv)
COPY . .

# Set Flask app path
ENV FLASK_APP=app.py

# Run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]