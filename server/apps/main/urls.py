
from django.urls import path

from server.apps.main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_collection, name='create_collection'),
    path(
        'collection/<int:collection_id>/',
        views.head_collection,
        name='head_collection',
    ),
    path(
        'collection/aggregate/<int:collection_id>/',
        views.aggregate_collection,
        name='aggregate_collection',
    ),
]
