from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='bookmarks'),
    path('add', views.add, name='bookmark-add'),
]
