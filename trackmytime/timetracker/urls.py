from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-entry', views.add, name='add'),
    path('stop-entry/<entry_id>', views.stop, name='stop'),
    path('overview', views.overview, name='overview'),
]
