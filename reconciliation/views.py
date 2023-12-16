from django.shortcuts import render, redirect
from .forms import SourceFileUploadForm, TargetFileUploadForm
from .models import SourceTargetFilePair, ReconciliationResults


def upload_files(request):
    source_form = SourceFileUploadForm(
        request.POST or None,
        request.FILES or None,
        prefix="source",
        target_type="Source",
    )
    target_form = TargetFileUploadForm(
        request.POST or None,
        request.FILES or None,
        prefix="target",
        target_type="Target",
    )

    if request.method == "POST":
        if source_form.is_valid() and target_form.is_valid():
            source_data = source_form.save()
            target_data = target_form.save()
            source_target_file_pair = SourceTargetFilePair.objects.create(
                source_file=source_data, target_file=target_data
            )
            return redirect(
                "get_reconciliation_report",
                source_target_file_pair_id=source_target_file_pair.pair_id,
            )

    context = {
        "source_form": source_form,
        "target_form": target_form,
    }
    return render(request, "reconciliation/upload_file.html", context)


def get_reconciliation_report(request, source_target_file_pair_id):
    if request.method == "GET":
        if source_target_file_pair_id:
            results = ReconciliationResults.objects.filter(
                source_target_file_pair__pair_id=source_target_file_pair_id
            ).all()
            context = {"results": results}
            return render(request, "reconciliation/report_template.html", context)
    else:
        return redirect("uploads")
