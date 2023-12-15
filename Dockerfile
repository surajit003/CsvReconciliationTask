FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
COPY requirements /app/

WORKDIR /app
RUN pip install -U "pip>=20.3.1" "setuptools>=49.2.1" "wheel>=0.34.2"
RUN pip install -r dev.txt

COPY . /app/

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
