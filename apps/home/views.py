# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from .forms import MarkForm
from .models import Mark, Bbr


@login_required(login_url="/login/")
def index(request):
    if request.method == 'POST':
        user = request.user
        bbr = Bbr.objects.get(user=user)
        mark = Mark(timestamp=datetime.now(), bbr=bbr)
        mark_form = MarkForm(request.POST, instance=mark)
        if mark_form.is_valid():
            mark_form.save()
            mark_form = MarkForm()
    else:
        mark_form = MarkForm()
    html_template = loader.get_template('home/index.html')
    context = {'segment': 'index',
               'mark_form': mark_form}
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def rechnung(request):
    query_results = []
    for bbr in Bbr.objects.all():
        query_results.append(bbr.get_marks())
    context = {'data': query_results}
    return render(request, 'home/rechnung.html', context)


