from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-entry', views.add, name='add'),
    path('stop-entry/<entry_id>', views.stop, name='stop'),
    path('delete-entry/<entry_id>', views.delete, name='delete'),
    path('overview', views.overview, name='overview'),
    path('clients', views.clients, name='clients'),
    path('unbooked', views.unbooked, name='unbooked'),
    path('unbooked-by-date', views.unbooked_by_date, name='unbooked-by-date'),
    path('mark-as-booked/<entry_id>', views.mark_as_booked, name='mark-as-booked'),
    path('mark-as-booked-by-date/<date>/<clientname>', views.mark_as_booked_by_date, name='mark-as-booked-by-date'),
]
