from django import forms
from django.core.files.storage import default_storage


class UploadForm(forms.Form):
    file = forms.FileField()