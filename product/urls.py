from django.urls import path
from product.views import (
    ProductCreateView,
    ProductListView,
    ProductVariantCombinationListView,
    ProductImageCreateView,
    ProductImageListView
)

urlpatterns = [
    path('lists/<uuid:store_id>/', ProductListView.as_view(), name='product-list'),
    path('create/<uuid:store_id>/', ProductCreateView.as_view(), name='product-create'),
    path('<uuid:product_id>/variants/lists/', ProductVariantCombinationListView.as_view(), name='product-variant-list'),
    path('<uuid:product_id>/images/create/', ProductImageCreateView.as_view(), name='product-image-create'),
    path('<uuid:product_id>/images/lists/', ProductImageListView.as_view(), name='product-image-list'),
]