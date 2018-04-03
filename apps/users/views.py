from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, UpdateView

AppUser = get_user_model()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['email', 'first_name', 'last_name', ]

    def get_success_url(self):
        return "{}?success=1".format(reverse("users:profile"))

    def get_object(self):
        return self.request.user


class UserListView(LoginRequiredMixin, TemplateView):
    template_name = "users/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = AppUser.objects.all()
        return context


class DashboardView(TemplateView):
    template_name = "backend/dashboard.html"
