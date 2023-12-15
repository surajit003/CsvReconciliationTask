import uuid
from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model class that provides self-updating
    ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FileUpload(TimeStampedModel):
    """
    Model to store uploaded files and their descriptions
    """

    TARGET_TYPE = (
        ("Source", "Source"),
        ("Target", "Target"),
    )
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="source_files/%Y/%m/%d/")
    target_type = models.CharField(max_length=10, choices=TARGET_TYPE, default="Source")

    class Meta:
        verbose_name = "Uploaded File"
        verbose_name_plural = "Uploaded Files"
        db_table = "uploaded_files"

    def __str__(self):
        return f"FileUpload - ID: {self.description}, Uploaded At: {self.created}"


class SourceTargetFilePair(models.Model):
    PROCESSING_STATUS = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    )
    pair_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    source_file = models.ForeignKey(
        "FileUpload", related_name="source_pair", on_delete=models.CASCADE
    )
    target_file = models.ForeignKey(
        "FileUpload", related_name="target_pair", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10, choices=PROCESSING_STATUS, default="Pending"
    )
    errors = models.JSONField(null=True, blank=True)

    def __str__(self):
        return (
            f"File Pair: {self.source_file.description} - "
            f"{self.target_file.description}"
        )

    class Meta:
        verbose_name = "Source Target File Pair"
        verbose_name_plural = "Source Target File Pairs"
        db_table = "source_target_file_pairs"


class SourceData(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    file_upload = models.ForeignKey(FileUpload, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Source Data"
        verbose_name_plural = "Source Data"
        db_table = "source_data"

    def __str__(self):
        return (
            f"SourceData - Name: {self.name}, Date: {self.date}, Amount: {self.amount}"
        )


class TargetData(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    file_upload = models.ForeignKey(FileUpload, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Target Data"
        verbose_name_plural = "Target Data"
        db_table = "target_data"

    def __str__(self):
        return (
            f"TargetData - Name: {self.name}, Date: {self.date}, Amount: {self.amount}"
        )


class ReconciliationResults(TimeStampedModel):
    type = models.CharField(max_length=100)
    record_identifier = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    source_value = models.TextField(null=True)
    target_value = models.TextField(null=True)
    source_target_file_pair = models.ForeignKey(
        SourceTargetFilePair, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Reconciliation Results"
        verbose_name_plural = "Reconciliation Results"
        db_table = "reconciliation_results"

    def __str__(self):
        return f"{self.type} - {self.record_identifier} - {self.field}"
