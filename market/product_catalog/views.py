from django.shortcuts import render
from django.views.generic import TemplateView

class ViewShows(TemplateView):
    template_name = 'market/base.jinja2'
