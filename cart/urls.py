from django.urls import path
from cart.views import CartDetailView, CartItemAddView, CartItemUpdateView

urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/items/add/', CartItemAddView.as_view(), name='cart-item-add'),
    path('cart/items/<uuid:cart_item_id>/update/', CartItemUpdateView.as_view(), name='cart-item-update'),
]