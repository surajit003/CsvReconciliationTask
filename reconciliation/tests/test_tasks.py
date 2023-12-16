from unittest.mock import patch

import pytest

from reconciliation.tests.factories import (
    FileUploadFactory,
    SourceTargetFilePairFactory,
)
from reconciliation.services.exceptions import InvalidFileHeaderError
from reconciliation.models import SourceTargetFilePair
from reconciliation.tasks import process_file

pytestmark = pytest.mark.django_db


@patch("reconciliation.tasks.csv_service.read_csv")
def test_process_file_succeeds(mock_read_csv):
    """
    Test that the process_file succeeds when the CSV file has the correct headers
    :param mock_read_csv:
    """
    FileUploadFactory()
    file_pair = SourceTargetFilePairFactory()

    mock_read_csv.side_effect = lambda file_upload, model, headers: None

    result = process_file(file_pair.id)
    assert result
    updated_file_pair = SourceTargetFilePair.objects.get(id=file_pair.id)
    assert updated_file_pair.status == "Completed"


@patch("reconciliation.tasks.csv_service.read_csv")
def test_process_file_fails_with_incorrect_headers(mock_read_csv):
    """
    Test that the process_file fails when the CSV file has incorrect headers
    :param mock_read_csv:
    """
    FileUploadFactory()
    file_pair = SourceTargetFilePairFactory()
    mock_read_csv.side_effect = InvalidFileHeaderError("CSV headers do not match")

    with pytest.raises(InvalidFileHeaderError) as exc:
        process_file(file_pair.id)
    assert isinstance(exc.value, InvalidFileHeaderError)
