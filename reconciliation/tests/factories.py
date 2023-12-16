import factory
from factory.django import DjangoModelFactory
from faker import Faker
from reconciliation.models import (
    FileUpload,
    SourceTargetFilePair,
    SourceData,
    TargetData,
    ReconciliationResults,
)

fake = Faker()


class FileUploadFactory(DjangoModelFactory):
    class Meta:
        model = FileUpload

    description = factory.Faker("text", max_nb_chars=50)
    file = factory.django.FileField(filename="example.txt")
    target_type = factory.Faker("random_element", elements=["Source", "Target"])


class SourceTargetFilePairFactory(DjangoModelFactory):
    class Meta:
        model = SourceTargetFilePair

    source_file = factory.SubFactory(FileUploadFactory)
    target_file = factory.SubFactory(FileUploadFactory)
    status = factory.Faker(
        "random_element", elements=["Pending", "Completed", "Failed"]
    )


class SourceDataFactory(DjangoModelFactory):
    class Meta:
        model = SourceData

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    date = factory.Faker("date")
    amount = factory.Faker("random_number")
    file_upload = factory.SubFactory(FileUploadFactory)


class TargetDataFactory(DjangoModelFactory):
    class Meta:
        model = TargetData

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    date = factory.Faker("date")
    amount = factory.Faker("random_number")
    file_upload = factory.SubFactory(FileUploadFactory)


class ReconciliationResultsFactory(DjangoModelFactory):
    class Meta:
        model = ReconciliationResults

    type = factory.Faker("word")
    record_identifier = factory.Faker("uuid4")
    field = factory.Faker("word")
    source_value = factory.Faker("text")
    target_value = factory.Faker("text")
    source_target_file_pair = factory.SubFactory(SourceTargetFilePairFactory)
