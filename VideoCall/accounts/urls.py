from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/',register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('avatar/', get_avatar, name='avatar'),
    path('logout/', logout_view, name='logout'),
    
] + static(settings.AVA_URL, document_root=settings.AVA_ROOT)
