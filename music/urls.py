from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('songs', views.songs, name='songs'),
    path('songs/<int:id>', views.songpost, name='songpost'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout_user', views.logout_user, name='logout_user'),
#    p ath('listenlater', views.listenlater, name='listenlater')
    path('watchlater', views.watchlater, name='watchlater')

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)