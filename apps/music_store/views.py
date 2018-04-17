from django.views.generic import FormView

from apps.music_store.forms import (
    AlbumUploadArchiveForm,
    handle_uploaded_archive,
)


class AlbumUploadArchiveView(FormView):
    """View for uploading archive with albums, which consist from tracks."""
    form_class = AlbumUploadArchiveForm
    template_name = 'music_store/album/upload_archive.html'
    success_url = '/admin/music_store/album/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES.get('file')
        if form.is_valid():
            handle_uploaded_archive(file)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Album Upload'
        return context
