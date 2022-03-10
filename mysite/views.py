from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def page_not_found(request, exception):
    response = render(request, 'mysite/404.html')
    response.status_code = 404
    return response
