import csv
from typing import Type

import structlog
from django.db.models import Model

from django.utils.dateparse import parse_date

from reconciliation.models import FileUpload
from reconciliation.services.exceptions import InvalidFileHeaderError

logger = structlog.get_logger(__name__)


def read_csv(
    file_upload: FileUpload, model: Type[Model], expected_headers: list
) -> list:
    """
    Read CSV file and save data to Source or Target model
    :param file_upload:
    :param model:
    :param expected_headers:
    :return:
    """
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
