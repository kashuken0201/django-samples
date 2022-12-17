from django.urls import path
from .views import *

urlpatterns = [
    path('list', list_view, name='list'),
    path('room', list_room_view, name='list_room'),
    path('room/<int:id>', room_detail, name="room_detail"),
    path('create', create_view, name='create_new_facility'),
    path('<int:id>', detail_view, name='detail_facility'),
    path('<int:id>/update', update_view, name='update_facility'),
    path('<int:id>/delete', delete_view, name='delete_facility'),
]