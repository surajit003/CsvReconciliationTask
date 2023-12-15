from django.urls import path
from .views import upload_files, get_reconciliation_report

urlpatterns = [
    path("uploads/", upload_files, name="uploads"),
    path(
        "reconciliation-results/<str:source_target_file_pair_id>/",
        get_reconciliation_report,
        name="get_reconciliation_report",
    ),
]
