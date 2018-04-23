import uuid

from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.music_store.forms import AlbumUploadArchiveForm
from .tasks import get_albums_from_zip, get_tracks_from_zip
from .utils import get_celery_task_status_info


class AlbumUploadArchiveView(FormView):
    """View for uploading archive with albums, which consist from tracks."""
    form_class = AlbumUploadArchiveForm
    template_name = 'music_store/album/upload_archive.html'

    def form_valid(self, form):
        """Override method to actions with a valid form data.

        Concretely, for send a uploaded archive to file handler.
        """
        file = form.files.get('file')
        filepath = default_storage.save(
            name=str(uuid.uuid4()),
            content=file
        )

        # save task_id in session
        task_id = get_tracks_from_zip.delay(filepath).task_id
        task_key = task_id.split("-")[0]
        self.request.session[task_key] = task_id

        return redirect(
            'admin:album_upload_status',
            task_key=task_key
        )

    def get_context_data(self, **kwargs):
        """Override method for add `title` in context."""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Albums Upload'
        return context


class TaskStatusView(View):
    """View for tracking status of uploading tasks."""

    def get(self, request, *args, **kwargs):
        """"""
        task_key = kwargs.get('task_key')
        task_data = get_celery_task_status_info(self.request, task_key)

        return JsonResponse(task_data)


class AlbumUploadStatusView(TemplateView):
    template_name = 'music_store/album/upload_archive_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_key = self.kwargs.get('task_key')
        task_data = get_celery_task_status_info(self.request, task_key)

        if not task_data['id']:
            raise HttpResponseNotFound

        context['task'] = task_data

        return context
