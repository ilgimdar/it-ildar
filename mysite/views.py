from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from articles.utils import DataMixin
from mysite.forms import RegisterUserForm


def page_not_found(request, exception):
    response = render(request, 'mysite/404.html')
    response.status_code = 404
    return response


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'mysite/register.html'
    success_url = reverse_lazy('login')
