# Use the official Python slim image as the base
FROM python:3.9-slim

# Set the working directory in the container
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Copy the Django project files to the working directory
COPY . .

# Expose the port on which Django will run (default is 8000)
EXPOSE 8000

# Run the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mindikatta.wsgi:application"]
