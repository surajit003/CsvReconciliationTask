from collections import defaultdict


from reconciliation.models import (
    SourceData,
    TargetData,
    ReconciliationResults,
    SourceTargetFilePair,
)


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
            if source_record.id == target_record.id:
                if source_record.name != target_record.name:
                    discrepancies.append(
                        ("Name", source_record.name, target_record.name)
                    )

                if source_record.date != target_record.date:
                    discrepancies.append(
                        ("Date", source_record.date, target_record.date)
                    )

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
