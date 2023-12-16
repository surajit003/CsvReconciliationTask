import io

import pytest
from unittest.mock import MagicMock
from reconciliation.services.csv_service import read_csv
from reconciliation.models import SourceData
from reconciliation.services.exceptions import InvalidFileHeaderError
from reconciliation.tests.factories import FileUploadFactory

pytestmark = pytest.mark.django_db


def test_read_csv_with_correct_headers():
    """
    Test that the read_csv function correctly reads a CSV file with the correct headers
    """
    file_upload = FileUploadFactory()
    expected_headers = ["ID", "Name", "Date", "Amount"]

    csv_content = "ID,Name,Date,Amount\n1,John,2023-01-01,100\n2,Alice,2023-01-02,200\n"

    file_upload.file.open = MagicMock(return_value=io.StringIO(csv_content))

    errors = read_csv(file_upload, SourceData, expected_headers)

    assert not errors

    assert SourceData.objects.count() == 2


def test_read_csv_with_incorrect_headers():
    """
    Test that the read_csv function raises an InvalidFileHeaderError when
    the CSV file has incorrect headers
    """
    file_upload = FileUploadFactory()
    expected_headers = [
        "ID",
        "Name",
        "Amount",
        "Date",
    ]

    csv_content = "ID,Name,Date,Amount\n1,John,2023-01-01,100\n2,Alice,2023-01-02,200\n"
    file_upload.file.open = MagicMock(return_value=io.StringIO(csv_content))

    with pytest.raises(InvalidFileHeaderError) as exc:
        read_csv(file_upload, SourceData, expected_headers)

    assert isinstance(exc.value, InvalidFileHeaderError)
