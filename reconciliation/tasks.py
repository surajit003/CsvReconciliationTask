import json
from typing import Optional

import structlog


from CSVReconcillationTask.celery import app
from reconciliation.models import (
    SourceData,
    TargetData,
    FileUpload,
    SourceTargetFilePair,
)
from reconciliation.services import reconciliation_service
from reconciliation.services import csv_service

logger = structlog.get_logger(__name__)


@app.task(name="process_file")
def process_file(file_pair_id: int) -> Optional[int]:
    """
    Process uploaded files and reconcile records
    :param file_pair_id:
    :return:

    TODO: This function is doing too much. It should be broken down into smaller functions.
    We could also use a class to encapsulate the logic or use an event based approach to decouple the logic.
    """

    try:
        source_target_file_pair = SourceTargetFilePair.objects.get(id=file_pair_id)
        source_file_upload = source_target_file_pair.source_file
        target_file_upload = source_target_file_pair.target_file
        source_file_upload_errors = csv_service.read_csv(
            source_file_upload, SourceData, ["ID", "Name", "Date", "Amount"]
        )
        target_file_upload_errors = csv_service.read_csv(
            target_file_upload, TargetData, ["ID", "Name", "Date", "Amount"]
        )

        if source_file_upload_errors or target_file_upload_errors:
            errors = json.dumps(
                {
                    "source_errors": source_file_upload_errors,
                    "target_errors": target_file_upload_errors,
                }
            )
            SourceTargetFilePair.objects.filter(id=file_pair_id).update(
                status="Completed", errors=errors
            )
        SourceTargetFilePair.objects.filter(id=file_pair_id).update(status="Completed")

        reconciliation_service.reconcile_records(source_target_file_pair.id)
        return source_target_file_pair.id
    except FileUpload.DoesNotExist:
        logger.error(f"FileUpload with id={file_pair_id} does not exist.")
        SourceTargetFilePair.objects.filter(id=file_pair_id).update(status="Failed")
        return None
