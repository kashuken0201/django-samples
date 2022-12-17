from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from accounts.models import *
from meeting.models import *

def index_view(request):
    user_id = request.session.get('user_id')
    if  user_id is not None:
        user = get_object_or_404(Account, id=user_id)
        rooms = Room.objects.filter(account = user)
        context = {
            'user': user,
            'rooms': rooms,
        }
        return render(request, 'home/meeting.html', context)
    else:
        if request.method == 'GET':
            return render(request, 'chat/join_room.html')
        else:
            room_id = request.POST.get('room_id')
            password = request.POST.get('password')
            username = request.POST.get('username')
            room = Room.objects.filter(id=room_id)
            if len(room) != 0:
                room = room[0]
                if room.password == password:
                    member = Member.objects.create(room=room, name=username)
                    return HttpResponseRedirect(reverse('room_user', args=(room.id, member.id)))
            context = { 'error': 'Room not found or password incorrect' }
            return render(request, 'chat/join_room.html', context)
