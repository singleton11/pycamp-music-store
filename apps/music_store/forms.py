
from django.forms import forms


class AlbumUploadArchiveForm(forms.Form):
    """Form for upload archive"""
    file = forms.FileField()
