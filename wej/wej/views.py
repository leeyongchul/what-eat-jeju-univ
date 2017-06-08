# wej/views.py
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

def my_view(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})