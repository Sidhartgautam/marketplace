from rest_framework import serializers
from product.models import (
    Product,
    ProductVariantCombination,
    ProductAttribute,
    ProductAttributeValue,
    ProductImage,
)

class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'attribute', 'value']


class ProductAttributeSerializer(serializers.ModelSerializer):
    values = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'values', 'store']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']


class ProductVariantCombinationSerializer(serializers.ModelSerializer):
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariantCombination
        fields = [
            'id', 'product', 'attribute_values', 'stock', 'price', 
            'discount_percentage', 'sku', 'is_active', 'image'
        ]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variant_combinations = ProductVariantCombinationSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    store = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id', 'store', 'category', 'name', 'slug', 'description', 
            'base_price', 'discount_percentage', 'sku', 'is_active', 
            'meta_title', 'meta_description', 'images', 'variant_combinations'
        ]
        read_only_fields = ['id', 'sku']