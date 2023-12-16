import pytest

from reconciliation.models import (
    SourceData,
    TargetData,
    ReconciliationResults,
)
from reconciliation.services.reconciliation_service import (
    reconcile_records,
)
from reconciliation.tests.factories import (
    SourceTargetFilePairFactory,
    FileUploadFactory,
)

pytestmark = pytest.mark.django_db


def test_reconcile_records_missing_in_target():
    """
    Test that the reconciliation service correctly identifies records that are missing in the files
    """
    source_data_file_upload = FileUploadFactory()
    target_data_file_upload = FileUploadFactory()
    file_pair = SourceTargetFilePairFactory(
        source_file=source_data_file_upload, target_file=target_data_file_upload
    )
    SourceData.objects.create(
        id=1,
        name="John",
        date="2023-01-01",
        amount=100,
        file_upload=source_data_file_upload,
    )
    TargetData.objects.create(
        id=2,
        name="Alice",
        date="2023-01-02",
        amount=200,
        file_upload=target_data_file_upload,
    )

    reconcile_records(file_pair.id)

    missing_value_results = ReconciliationResults.objects.all()

    assert missing_value_results.count() == 2
    assert missing_value_results[0].type == "Missing in Target"
    assert missing_value_results[0].source_value
    assert missing_value_results[0].target_value is None
    assert missing_value_results[0].source_target_file_pair == file_pair

    assert missing_value_results[1].type == "Missing in Source"
    assert missing_value_results[1].source_value
    assert missing_value_results[1].target_value is None
    assert missing_value_results[1].source_target_file_pair == file_pair


def test_reconcile_records_field_discrepancy():
    """
    Test that the reconciliation service correctly identifies field discrepancies
    """
    source_data_file_upload = FileUploadFactory()
    target_data_file_upload = FileUploadFactory()
    file_pair = SourceTargetFilePairFactory(
        source_file=source_data_file_upload, target_file=target_data_file_upload
    )
    SourceData.objects.create(
        id=1,
        name="John",
        date="2023-01-01",
        amount=100,
        file_upload=source_data_file_upload,
    )
    TargetData.objects.create(
        id=1,
        name="Alice",
        date="2023-01-01",
        amount=200,
        file_upload=target_data_file_upload,
    )

    reconcile_records(file_pair.id)

    field_discrepancy = ReconciliationResults.objects.all()
    assert field_discrepancy.count() == 2
    assert field_discrepancy[0].type == "Field Discrepancy"
    assert field_discrepancy[0].field == "Name"
    assert field_discrepancy[0].source_value == "John"
    assert field_discrepancy[0].target_value == "Alice"

    assert field_discrepancy[1].type == "Field Discrepancy"
    assert field_discrepancy[1].field == "Amount"
    assert field_discrepancy[1].source_value == "100.00"
    assert field_discrepancy[1].target_value == "200.00"
