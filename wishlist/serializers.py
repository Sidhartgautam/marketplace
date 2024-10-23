from rest_framework import serializers
from wishlist.models import Wishlist, WishlistItem
from product.models import Product

class WishlistItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = WishlistItem
        fields = ['id', 'product']

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'items']
        read_only_fields = ['id', 'user', 'items']