from django.views.generic import FormView

from apps.music_store.forms import TrackUploadArchiveForm, \
    handle_uploaded_archive


class TrackUploadArchiveView(FormView):
    form_class = TrackUploadArchiveForm
    template_name = 'music_store/track/upload_archive.html'
    success_url = '/admin/music_store/track/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES.get('file')
        if form.is_valid():
            handle_uploaded_archive(file)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

