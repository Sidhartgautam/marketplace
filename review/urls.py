from django.urls import path
from review.views import ProductReviewCreateView, ProductReviewListView

urlpatterns = [
    path('products/<uuid:product_id>/reviews/lists/', ProductReviewListView.as_view(), name='product-review-list'),
    path('products/<uuid:product_id>/reviews/create/', ProductReviewCreateView.as_view(), name='product-review-create'),
]