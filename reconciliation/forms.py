from django import forms
from .models import FileUpload


class SourceFileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        target_type = kwargs.pop("target_type", None)
        super(SourceFileUploadForm, self).__init__(*args, **kwargs)
        if target_type:
            self.fields["target_type"].initial = target_type
            self.fields["target_type"].widget = forms.HiddenInput()

    class Meta:
        model = FileUpload
        fields = ["description", "file", "target_type"]
        labels = {
            "description": "Source File Description",
            "file": "Upload Source File",
        }


class TargetFileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        target_type = kwargs.pop("target_type", None)
        super(TargetFileUploadForm, self).__init__(*args, **kwargs)
        if target_type:
            self.fields["target_type"].initial = target_type
            self.fields["target_type"].widget = forms.HiddenInput()

    class Meta:
        model = FileUpload
        fields = ["description", "file", "target_type"]
        labels = {
            "description": "Target File Description",
            "file": "Upload Target File",
        }
