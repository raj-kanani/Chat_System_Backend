FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files to the working directory
COPY . /usr/src/app/

# Set the default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
