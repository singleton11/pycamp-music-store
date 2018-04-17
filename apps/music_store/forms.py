from tempfile import NamedTemporaryFile

from django.forms import forms


class AlbumUploadArchiveForm(forms.Form):
    """Form for upload archive"""
    file = forms.FileField()


def handle_uploaded_archive(file):
    """Handler uploaded file. Here unpack zip file and create tracks and albums

    """
    with NamedTemporaryFile() as tmp_file:
        """working with archive `tmp_file`. 
        
        Notice: after exit from `with` blok, file will be deleted.
        """
        for chunk in file.chunks():
            tmp_file.write(chunk)

        # Work with `tmp_file` here
        print(tmp_file)
