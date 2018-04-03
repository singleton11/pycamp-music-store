from django.core.files import File


class JSONFile(File):
    content_type = "application/json"
