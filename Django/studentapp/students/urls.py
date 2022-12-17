from django.urls import path
from .views import detail_view, create_view, update_view, delete_view, list_view

urlpatterns = [
    path('', list_view, name='list'),
    path('create', create_view, name='create'),
    path('<int:id>', detail_view, name='detail'),
    path('<int:id>/update', update_view, name='update'),
    path('<int:id>/delete', delete_view, name='delete'),
]