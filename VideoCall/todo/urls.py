from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', todo_view, name='todo'),
    path('<int:id>', todo_detail_view, name='todo_detail'),
    path('create', create_new_todo_view, name='create_todo'),

    path('<int:id>/delete', delete_todo_view, name='delete_todo'),
    path('<int:id>/deleteall', delete_all_item_view, name='delete_all_item'),
    path('<int:id>/sort', sort_item_view, name='sort_item'),
    path('search', search_item_view, name='search_item'),

    path('item/create', create_item_view, name='create_item'),
    path('item/<int:id>/delete', delete_item_view, name='delete_item'),
]