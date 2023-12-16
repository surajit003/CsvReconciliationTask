# CSV Reconciliation

This repository contains a simple reconciliation app designed to compare CSV files and identify differences.

## Setup

### Requirements

- Python (version): Python 3.10.0
- PyCharm: IDE used for development.
- PostgreSQL: Database system used for this project.
- pre-commit: Tool for managing and maintaining multi-language pre-commit hooks.

### Installation

1. **Python Setup:** Create a virtual environment and activate it.

   ```bash
   python -m venv venv_name
   source venv_name/bin/activate  # For Linux/Mac
   venv_name\Scripts\activate  # For Windows
   ```

2. **Install Dependencies:** Use `pip` to install project dependencies from `requirements/dev.txt`.

   ```bash
   pip install -r requirements/dev.txt
   ```

3. **Database Setup:** Set up a PostgreSQL database and configure settings in Django's `settings.py`.

4. **PyCharm Setup:** Open the project in PyCharm and configure the project interpreter to use the created virtual environment.

5. **Pre-commit Hook Setup:** Install and set up pre-commit hooks to maintain code quality.

   ```bash
   pre-commit install
   ```

## Running the Project

1. **Database Migrations:** Run database migrations with the following command:
   
  ```
   psql -U postgres -c "CREATE DATABASE reconciliation_dev"
   ```

   ```bash
   python manage.py migrate
   ```

3. **Run Django Server:** Start the Django development server:

   ```bash
   python manage.py runserver
   ```

4. **Run Celery Worker:** Initiate the Celery worker:

   ```bash
   celery -A CSVReconcillationTask.celery worker -l info
   ```

5. **Accessing the Application:** Access the application via `http://localhost:8000` in a web browser.

6. Endpoints:

   - `/csv-reconciliation/tunnel`: Django admin panel.
   - `/api/v1/uploads`: FileUpload Endpoint.
   - `/api/v1/reconciliation-results/<str:source_target_file_pair_id>`: Reconciliation Report.

### Docker

If Docker is installed, run the project using:

```bash
docker-compose up --build
```

#### Improvements

- Design a better UI.
  The UI has been built using the Django template engine. A better UI can be designed using a frontend framework
  like React or Vue Considering the API will be headless, a frontend framework will be a better choice.

- Saving the csv data in the SourceData and TargetData Table.
  The current implementation saves the csv data one by one in a loop. However, this can be improved by saving
  the data using bulk_create.
  Caveat - 1. Rollback will not be possible if any of the data fails to save.

- Application Design
  Currently, the application is designed using the MVT pattern. However, the application can be designed using
  the DDD pattern to make it more scalable and maintainable.

- Authentication
  The application does not have any authentication. This can be added using JWT or OAuth2.

- Authorization
  The application does not have any authorization. This can be added using Django's permission system.

- Event Driven Architecture
  The application can be designed using an event-driven architecture. This will help in decoupling the application
  and make it more scalable.

  e.g - The application can be designed using a message broker like RabbitMQ. The file upload can be published as an
  event and the reconciliation service can subscribe to the event.

  The reconciliation service can publish the reconciliation result as an event and the client
  can subscribe to the event.

- API Documentation
  The API documentation can be generated using Swagger or Redoc.

- Unit Tests
  The application has the bare minimum unit tests. More unit tests can be added to improve the test coverage.

- Integration Tests

  - The application does not have any integration tests. Integration tests can be added to test the integration between the different components of the application. We can use a library like behave.

- Performance Tests
  The application does not have any performance tests. Performance tests can be added to test the performance of the application under load. We can use load forge to test the performance of the application.

- Logging
  The application does not have any logging to external service. Logging can be added to log the application's events. We can use a library like Sentry to log the application's events.

- APM (Application Performance Monitoring)
  The application does not have any APM. APM can be added to monitor the application's performance. We can use a library like datadog or newrelic to monitor the application's performance.

- API Versioning
  The API versioning is kept to a bare minimum. The API versioning can be improved by versioning the modules and the endpoints.

- CI/CD
  The application does not have any CI/CD. CI/CD can be added to automate the build and deployment process. We can use a tool like Jenkins or Github/Gitlab Actions to automate the build and deployment process.

  - Linting
  - Unit Tests
  - Integration Tests
  - Deployment

- S3 storage
  Currently, the csv files are stored in the local file system. However, this can be improved by storing
  the csv files in S3 storage.

##### Important Note

    Once the file is uploaded, the file is processed in the background using celery. The reconciliation report will
    not immediately be available.There is currently a 5-second refresh which will automatically refresh the page
    every 5 seconds. This can be improved by using web sockets.
    In an ideal scenario, we will have a progress bar which will show the progress of the reconciliation process.
    Once the reconciliation process is complete, the reconciliation report will be available.

##### Assumptions

The following assumptions have been made while designing the application:

- The CSV files weren't processed in memory. This is because the CSV files can be large and processing them in
  memory can cause memory issues.
- We could use a batch-size which is being determined by the size of the file and then we could do
  a batch processing in chunks along with bulk insert to reduce the number of db calls.
- Django Finite State Machine should be used to control the status of the File Upload Status.
