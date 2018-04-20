from django.views import View
from django.http import HttpResponse

from django.core.files.storage import default_storage
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.music_store.forms import AlbumUploadArchiveForm
from .tasks import get_albums_from_zip
import uuid
import json
from config.celery import app


class AlbumUploadArchiveView(FormView):
    """View for uploading archive with albums, which consist from tracks."""
    form_class = AlbumUploadArchiveForm
    template_name = 'music_store/album/upload_archive.html'
    success_url = '/admin/music_store/album/'

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
        task_id = get_albums_from_zip.delay(filepath).task_id
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

    def get(self, request, task_id, *args, **kwargs):
        """"""
        task_id = kwargs.get('task_key')
        task_status = app.AsyncResult(task_id).state
        task_result = app.AsyncResult(task_id).result

        task_data = {
            'task_id': task_id,
            'task_status': task_status,
            'task_result': task_result
        }

        return HttpResponse(json.dumps(task_data), mimetype='application/json')


class AlbumUploadStatusView(TemplateView):
    template_name = 'music_store/album/upload_archive_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task_key = self.kwargs['task_key']
        task_id = self.request.session.get(task_key)

        if task_id == None:
            raise HttpResponseNotFound

        context['task_id'] = task_id
        context['task_status'] = app.AsyncResult(task_id).state
        context['task_result'] = app.AsyncResult(task_id).result
        return context
