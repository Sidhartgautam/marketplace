from django.contrib import admin

# Register your models here.
from .models import Product, ProductVariantCombination, ProductImage, ProductAttribute, ProductAttributeValue,Category


admin.site.register(Product)
admin.site.register(ProductVariantCombination)
admin.site.register(ProductImage)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Category) 
