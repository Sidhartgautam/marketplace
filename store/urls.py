from django.urls import path
from .views import StoreListView, StoreCreateView

urlpatterns = [
    path('list/', StoreListView.as_view(), name='store_list'),
    path('create/', StoreCreateView.as_view(), name='store_create'),
]