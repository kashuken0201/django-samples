from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', meeting_view, name='meeting'),
    path('room/create', create_room_view, name='create_room'),
    path('room/<int:room_id>/<int:user_id>/', room_user_view, name='room_user'),
    path('room/join/', join_room_view, name='join_room'), 

    path('room/<int:room_id>/', room_view, name='room'),
    path('room/<int:room_id>/delete/', delete_room_view, name='delete_room'),
    
    path('member/<int:user_id>/delete/', delete_member_view, name='delete_member'),
]

