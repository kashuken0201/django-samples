from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from .forms import *
from .models import *
import zlib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = zlib.crc32(form.cleaned_data['password'].encode())
        if Account.objects.filter(username=username, password=password).exists():
            user_id = Account.objects.get(username=username, password=password).id
            request.session['user_id'] = user_id
            return HttpResponseRedirect(reverse('meeting'))
        context = { 'error': 'Invalid username or password', 'form': form }
        return render(request, 'chat/login.html', context)
    return render(request, 'chat/login.html', {'form': form})

def register_view(request):
    if request.method == 'GET':
        return render(request, 'chat/register.html')
    else:
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        password = (request.POST.get('password'))
        checkPassword = (request.POST.get('checkPassword'))
        if password == checkPassword and password!='' and username!='' and fullname !='':
            if not Account.objects.filter(username=username).exists():
                Account.objects.create(username=username, password=zlib.crc32(password.encode()),fullname=fullname)
                return HttpResponseRedirect(reverse('login'))
            else:
                context = { 'error': 'username already exist' }
        else :
            context = { 'error': 'password and password again dissimilarity' }
        return render(request, 'chat/register.html',context)

def logout_view(request):
    if request.session.get('user_id') is None:
        return HttpResponseRedirect(reverse('login'))
    else:
        del request.session['user_id']
        return HttpResponseRedirect(reverse('login'))

def profile_view(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.method=='GET':
            user = Account.objects.get(id=user_id)
            initial_value = {
                'fullname' : user.fullname,
                'email': user.email,
                'phone': user.phone,
                'age': user.age,
                'avatar': user.avatar
            }
            form = ProfileForm(request.POST or None, initial=initial_value)
            context = {
                'user': user,
                'form': form
            }
            return render(request, 'home/profile.html', context)
        else:
            form = ProfileForm(request.POST or None, request.FILES)
            if form.is_valid():
                fullname = form.cleaned_data['fullname']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                age = form.cleaned_data['age']
                avatar = form.cleaned_data['avatar']
                try:
                    if phone:
                        int(phone)
                    user = Account.objects.get(id=user_id)
                    user.fullname=fullname
                    user.email=email
                    user.phone=phone
                    user.age=age
                    if avatar:
                        user.avatar=avatar
                    else:
                        user.avatar=Account._meta.get_field('avatar').get_default()
                    user.save()
                    return HttpResponseRedirect(reverse('profile'))
                except:
                    return HttpResponseRedirect(reverse('profile'))
            else:
                return HttpResponseRedirect(reverse('profile'))

def get_avatar(request):
    user_id = request.session.get('user_id')
    user = Account.objects.get(id=user_id)
    src = user.avatar
    return HttpResponse(src)