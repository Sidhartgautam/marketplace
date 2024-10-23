# wishlist/urls.py
from django.urls import path
from wishlist.views import WishlistDetailView, WishlistItemAddView, WishlistItemRemoveView

urlpatterns = [
    path('', WishlistDetailView.as_view(), name='wishlist-detail'),
    path('items/add/', WishlistItemAddView.as_view(), name='wishlist-item-add'),
    path('items/<uuid:pk>/remove/', WishlistItemRemoveView.as_view(), name='wishlist-item-remove'),
]
