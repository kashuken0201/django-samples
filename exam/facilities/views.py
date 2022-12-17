from django.shortcuts import render, redirect, get_object_or_404
from .models import Facilities, Room
from .forms import FacilitiesForm

# Create your views here.
def create_view(request):
    initial_value = {
        'facility_name': 'Ghế',
        'quantity': '10',
    }
    form = FacilitiesForm(request.POST or None, initial=initial_value)
    if form.is_valid():
        form.save()
        return redirect('/facilities/list')
    context = {'form': form}
    return render(request, 'create_new_facility.html', context)

def update_view(request, id):
    food = get_object_or_404(Facilities, id=id)
    form = FacilitiesForm(request.POST or None, instance=food)
    if form.is_valid():
        form.save()
        return redirect('/facilities/list')
    context = {'form': form}
    return render(request, 'create_new_facility.html', context)

def delete_view(request, id):
    facility = get_object_or_404(Facilities, id=id)
    if request.method == 'POST':
        facility.delete()
        return redirect('/facilities/list')
    context = {'facility': facility}
    return render(request, 'delete_facility.html', context)


def detail_view(request, id):
    facility = get_object_or_404(Facilities, id=id)
    context = {'facility': facility}
    return render(request, 'detail_facility.html', context)


def list_view(request):
    keyword = request.GET.get('keyword')
    if keyword:
        facilities = Facilities.objects.filter(facility_name=keyword)
    else:
        facilities = Facilities.objects.all()
    context = {
        'facilities': facilities,
        'keyword':keyword
    }
    return render(request, 'facility_list.html', context)

def room_detail(request, id):
    room = Room.objects.get(id=id)
    facilities = Facilities.objects.filter(room__id=id)
    context = {
        'room': room,
        'facilities': facilities
    }
    return render(request, 'room_detail.html', context)

def list_room_view(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'room_list.html', context)

