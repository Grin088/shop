from django.shortcuts import render  # noqa F401
from django.views.generic import TemplateView
# Create your views here.


class BaseView(TemplateView):
    template_name = 'market/base.jinja2'
