from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    context = {
        'name': 'an Trinh',
        'skills': ['c#', 'html', 'django'],
        'content': '<div class="alert alert-primary" role="alert">Hi Django!</div>'
    }
    return render(request, 'home.html', context)


def contact_view(request):
    return render(request, 'contact.html', {})


def about_view(request):
    return render(request, 'about.html', {})
