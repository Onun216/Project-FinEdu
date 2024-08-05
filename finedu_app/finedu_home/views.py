from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def home(request):
    template = loader.get_template('finedu_home/pages/index.html')
    return HttpResponse(template.render())
