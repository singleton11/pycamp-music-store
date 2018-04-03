from django.http import JsonResponse


class PaginatedSortedFilteredListView(object):

    def get_paginate_by(self, queryset):
        return self.request.GET.get('limit', self.paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', None)
        if search:
            queryset = queryset.filter(last_name__icontains=search)
        return queryset

    def get_ordering(self):
        order = self.request.GET.get('order', None)
        if order:
            return (order, )
        return self.ordering


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView).

    Sample:
    class UserListView(AjaxableResponseMixin,
                       PaginatedSortedFilteredListView,
                       ListView):
        model = get_user_model()
        serializer_class = CustomUserDetailSerializer
        paginate_by = 1
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {'pk': self.object.pk, }
            return JsonResponse(data)
        else:
            return response

    def get(self, request, *args, **kwargs):
        ret = super().get(request, *args, **kwargs)
        if request.is_ajax():
            try:
                data = self.serializer_class(self.object).data
            except AttributeError:
                ctx = ret.context_data['object_list']
                data = self.serializer_class(ctx, many=True).data
                if not hasattr(self, 'flat'):
                    data = dict(total=self.get_queryset().count(), rows=data)
            return JsonResponse(data, safe=False)
        return ret
