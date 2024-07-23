FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy just the requirements file first to leverage Docker cache
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]


