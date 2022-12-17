from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from .forms import *
import zlib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse

from .models import *

# Create your views here.
def meeting_view(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        user = get_object_or_404(Account, id=user_id)
        rooms = Room.objects.filter(account = user)
        context = {
            'user': user,
            'rooms': rooms,
        }
        return render(request, 'home/meeting.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))

def room_view(request, room_id):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('/login/')
    else:
        room = get_object_or_404(Room, id=room_id)
        user = get_object_or_404(Account, id=user_id)
        member = Member.objects.create(name = user.username, room = room)
        return HttpResponseRedirect(reverse('room_user', args=(room.id, member.id)))

def room_user_view(request, room_id, user_id):
    room = get_object_or_404(Room, id=room_id)
    user = get_object_or_404(Member, id=user_id)
    context = {
        'room': room,
        'user': user,
    }
    return render(request, 'chat/main.html', context)

def create_room_view(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            room_name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = get_object_or_404(Account, id=request.session.get('user_id'))
            room = Room.objects.create(name=room_name, password=password, account= user)
            member = Member.objects.create(room = room, name = user.username)
            return HttpResponseRedirect(reverse('room_user', args=(room.id, member.id)))
    return render(request, 'chat/create_room.html', {'form': form})

def join_room_view(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room = Room.objects.filter(id=room_id)
        if room.exists():
            room = room[0]
            if room.password == request.POST.get('password'):
                user = get_object_or_404(Account, id=request.session.get('user_id'))
                member = Member.objects.create(room = room, name = user.fullname)
                return HttpResponseRedirect(reverse('room_user', args=(room.id, member.id)))
        else:
            context = {
                'error': 'Room not found or password is incorrect.',
            }
            return render(request, 'chat/join_room.html', context)
    return render(request, 'chat/join_room.html')
        
def delete_room_view(request, room_id):
    try:
        room_id = int(room_id)
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return redirect('/')
    except:
        return redirect('/')

@csrf_exempt
def delete_member_view(request, user_id):
    member = get_object_or_404(Member, id=user_id)
    member.delete()
    return JsonResponse('Member deleted', safe=False) 