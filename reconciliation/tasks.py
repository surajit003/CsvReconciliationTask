import csv
import json
import structlog
from collections import defaultdict

from django.utils.dateparse import parse_date

from CSVReconcillationTask.celery import app
from reconciliation.exceptions import InvalidFileHeaderError
from reconciliation.models import (
    SourceData,
    TargetData,
    FileUpload,
    ReconciliationResults,
    SourceTargetFilePair,
)

logger = structlog.get_logger(__name__)


def read_csv(file_upload, model, expected_headers):
    errors = []
    try:
        file_to_read = file_upload.file
        with file_to_read.open(mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            actual_headers = csv_reader.fieldnames
            if actual_headers != expected_headers:
                logger.error("CSV headers do not match the expected headers.", actual_headers=actual_headers,
                             expected_headers=expected_headers)
                raise InvalidFileHeaderError("CSV headers do not match the expected headers.")

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
    except Exception as e:
        logger.error(f"Error reading csv error: {e}")
    return errors


def reconcile_records(source_target_file_pair_id):
    source_target_file_pair = SourceTargetFilePair.objects.filter(
        id=source_target_file_pair_id
    ).first()
    source_records = SourceData.objects.filter(
        file_upload=source_target_file_pair.source_file
    )
    target_records = TargetData.objects.filter(
        file_upload=source_target_file_pair.target_file
    )

    reconciliation_results = defaultdict(list)

    for record_type, records in [
        ("Missing in Target", source_records),
        ("Missing in Source", target_records),
    ]:
        for record in records:
            matching_record = (
                target_records.filter(id=record.id).first()
                if record_type == "Missing in Target"
                else source_records.filter(id=record.id).first()
            )

            if not matching_record:
                reconciliation_results[record_type].append(
                    {
                        "record_identifier": record.id,
                        "field": "ID",
                        "source_value": str(record),
                        "target_value": None,
                        "source_target_file_pair": source_target_file_pair,
                    }
                )

    for record_type, source, target in [
        ("Field Discrepancy", source_records, target_records)
    ]:
        for source_record, target_record in zip(source, target):
            discrepancies = []
            if source_record.name != target_record.name:
                discrepancies.append(("Name", source_record.name, target_record.name))

            if source_record.date != target_record.date:
                discrepancies.append(("Date", source_record.date, target_record.date))

            if source_record.amount != target_record.amount:
                discrepancies.append(
                    ("Amount", source_record.amount, target_record.amount)
                )

            if discrepancies:
                for field, source_value, target_value in discrepancies:
                    reconciliation_results[record_type].append(
                        {
                            "record_identifier": source_record.id,
                            "field": field,
                            "source_value": source_value,
                            "target_value": target_value,
                            "source_target_file_pair": source_target_file_pair,
                        }
                    )

    for result_type, results in reconciliation_results.items():
        for result in results:
            ReconciliationResults.objects.create(
                type=result_type,
                record_identifier=result["record_identifier"],
                field=result["field"],
                source_value=result["source_value"],
                target_value=result["target_value"],
                source_target_file_pair=source_target_file_pair,
            )


@app.task(name="process_file")
def process_file(file_upload_id):
    try:
        source_target_file_pair = SourceTargetFilePair.objects.get(id=file_upload_id)
        source_file_upload = source_target_file_pair.source_file
        target_file_upload = source_target_file_pair.target_file
        source_file_upload_errors = read_csv(
            source_file_upload, SourceData, ["ID", "Name", "Date", "Amount"]
        )
        target_file_upload_errors = read_csv(
            target_file_upload, TargetData, ["ID", "Name", "Date", "Amount"]
        )

        if source_file_upload_errors or target_file_upload_errors:
            errors = json.dumps(
                {
                    "source_errors": source_file_upload_errors,
                    "target_errors": target_file_upload_errors,
                }
            )
            SourceTargetFilePair.objects.filter(id=file_upload_id).update(
                status="Completed", errors=errors
            )
        SourceTargetFilePair.objects.filter(id=file_upload_id).update(
            status="Completed"
        )

        reconcile_records(source_target_file_pair.id)
        return source_target_file_pair.id
    except FileUpload.DoesNotExist:
        logger.error(f"FileUpload with id={file_upload_id} does not exist.")
        SourceTargetFilePair.objects.filter(id=file_upload_id).update(status="Failed")
        return None
