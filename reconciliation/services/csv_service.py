import csv
import structlog

from django.utils.dateparse import parse_date

from reconciliation.services.exceptions import InvalidFileHeaderError

logger = structlog.get_logger(__name__)


def read_csv(file_upload, model, expected_headers):
    errors = []
    try:
        file_to_read = file_upload.file
        with file_to_read.open(mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            actual_headers = csv_reader.fieldnames
            if actual_headers != expected_headers:
                logger.error(
                    "CSV headers do not match the expected headers.",
                    actual_headers=actual_headers,
                    expected_headers=expected_headers,
                )
                raise InvalidFileHeaderError(
                    "CSV headers do not match the expected headers."
                )

            for row in csv_reader:
                transformed_row = {
                    "id": row["ID"],
                    "name": row["Name"].title(),
                    "date": parse_date(row["Date"]),
                    "amount": float(row["Amount"]),
                    "file_upload": file_upload,
                }
                instance = model(**transformed_row)
                instance.save()
    except FileNotFoundError as e:
        logger.error(f"Error reading CSV: {e}")
    except ValueError as e:
        logger.error(f"Value error: {e}")

    return errors
