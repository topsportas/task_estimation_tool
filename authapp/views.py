from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from .forms import CreateUserForm


class UserLoginView(LoginView):
    template_name = "authapp/login.html"


class UserCreateView(FormView):
    template_name = "authapp/register.html"
    form_class = CreateUserForm
    success_url = "/auth/login/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
