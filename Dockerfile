# Base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install libs
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Do not hardcode tokens here; Koyeb will set env vars
ENV BOT_TOKEN=""
ENV OWNER_ID=""

# Run the bot
CMD ["python", "bot.py"]
