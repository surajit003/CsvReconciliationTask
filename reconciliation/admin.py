from django.contrib import admin

from .models import (
    SourceData,
    TargetData,
    FileUpload,
    ReconciliationResults,
    SourceTargetFilePair,
)


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ("description", "file", "created", "modified")
    search_fields = ("description",)


@admin.register(SourceTargetFilePair)
class FilePairAdmin(admin.ModelAdmin):
    list_display = (
        "get_source_description",
        "get_target_description",
        "status",
    )
    non_editable_fields = ("status",)

    def get_source_description(self, obj):
        return obj.source_file.description if obj.source_file else ""

    get_source_description.short_description = "Source Description"

    def get_target_description(self, obj):
        return obj.target_file.description if obj.target_file else ""

    get_target_description.short_description = "Target Description"


@admin.register(SourceData)
class SourceDataAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date", "amount", "created", "modified")
    search_fields = ("name", "date")
    list_filter = ("date", "created", "modified")


@admin.register(TargetData)
class TargetDataAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date", "amount")
    search_fields = ("name", "date")
    list_filter = ("date",)


@admin.register(ReconciliationResults)
class ReconciliationResultsAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "record_identifier",
        "field",
        "source_value",
        "target_value",
        "get_source_target_file_pair",
    )

    def get_source_target_file_pair(self, obj):
        return obj.source_target_file_pair.id

    search_fields = (
        "type",
        "record_identifier",
        "field",
        "source_value",
        "target_value",
    )
    list_filter = ("type", "field")
