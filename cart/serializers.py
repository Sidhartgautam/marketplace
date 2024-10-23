from rest_framework import serializers
from cart.models import Cart, CartItem
from product.models import ProductVariantCombination

class CartItemSerializer(serializers.ModelSerializer):
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariantCombination.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'quantity', 'get_total_price']
        read_only_fields = ['id', 'get_total_price']

    def validate_quantity(self, value):
        # Retrieve the product_variant object
        product_variant_id = self.initial_data.get('product_variant')
        try:
            product_variant = ProductVariantCombination.objects.get(id=product_variant_id)
        except ProductVariantCombination.DoesNotExist:
            raise serializers.ValidationError("Invalid product variant.")

        # Now check the stock of the product_variant
        if value > product_variant.stock:
            raise serializers.ValidationError("Not enough stock available.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField(source='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'is_active', 'total_price']
        read_only_fields = ['id', 'user', 'is_active', 'total_price']
