from django.http import HttpResponseServerError, HttpResponseNotFound
from django.template.loader import render_to_string

def custom_error_page(request):
    return HttpResponseServerError(
        render_to_string('500.html', request=request))


def custom_not_found_page(request):
    return HttpResponseNotFound(
        render_to_string('404.html', request=request))