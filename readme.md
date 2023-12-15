# CSV Reconciliation

A simple reconciliation app to compare csv and find out the differences.

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

2. **Install Dependencies:** Use `pip` to install project dependencies from `requirements.txt`.

    ```bash
    pip install -r requirements/dev.txt
    ```

3. **Database Setup:** Set up a PostgreSQL database and configure settings in Django's `settings.py`.

4. **PyCharm Setup:** Open the project in PyCharm and configure the project interpreter to use the created virtual environment.

5. **pre-commit Hook Setup:** Install and set up pre-commit hooks to maintain code quality.

    ```bash
    pre-commit install
    ```

## Running the Project

1. **Run Django Server:** Use the following command to start the Django development server:

    ```bash
    python manage.py runserver
    ```

2. **Accessing the Application:** Access the application via `http://localhost:8000` in a web browser.

3. Endpoints:

    - `/csv-reconciliation/tunnel`: Django admin panel.
    - `/api/v1/uploads`: FileUpload Endpoint.
    - `/api/v1/reconciliation-results/<str:source_target_file_pair_id>`: Reconciliation Report.

#### Docker
If you have docker installed, you can run the project using the following command:
```bash
docker-compose up --build
```