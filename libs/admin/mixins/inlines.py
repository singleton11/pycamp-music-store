from .model_admin import ForbidDeleteAdd


class NonEditableInline(ForbidDeleteAdd):
    extra = 0
    max_num = 0
