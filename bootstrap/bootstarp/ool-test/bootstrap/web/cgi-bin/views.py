#!/usr/bin/env python
# coding: utf-8
from django.http import HttpResponse
from django.template import Context, loader

def index(request):
	context = Context()
	t = loader.get_template('index.html')
	return HttpResponse(t.render(context))
