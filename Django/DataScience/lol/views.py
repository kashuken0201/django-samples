from unittest import result
from django.shortcuts import render, redirect
from .models import *
# Create your views here.

def index_view(request):
    champs = Champion.objects.all()
    if request.method == 'POST':
        blue_champs = []
        red_champs = []
        for i in range(5):
            blue_champs.append(request.POST.get('b' + str(i+1)))
            red_champs.append(request.POST.get('r' + str(i+1)))
        result = 10
        return render(request, 'meeting.html', {'champs': champs, 'result':result})
    return render(request, 'meeting.html', {'champs': champs})