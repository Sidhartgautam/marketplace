from django.db import models
from store.models import Store
from core.utils.models import UUIDModel, TimeStampedModel
from django.core.exceptions import ValidationError

# Category Model
class Category(UUIDModel, TimeStampedModel):
    store=models.ForeignKey(Store, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('store', 'slug')


# Product Model
class Product(UUIDModel, TimeStampedModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_in_category')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_final_price(self):
        if self.discount_percentage:
            return self.base_price * (1 - (self.discount_percentage / 100))
        return self.base_price


# Product Attribute Model
class ProductAttribute(UUIDModel, TimeStampedModel): 
    store=models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_attributes', null=True,blank=True)
    name = models.CharField(max_length=255)  # e.g., Color, Size

    def __str__(self):
        return self.name


# Product Attribute Value Model
class ProductAttributeValue(UUIDModel, TimeStampedModel):
    store=models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_attribute_values', null=True,blank=True)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)  # e.g., "Red", "Blue", "Large"
    

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


# Product Variant Combination Model
class ProductVariantCombination(UUIDModel, TimeStampedModel):
    store=models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_variant_combinations', null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant_combinations')
    attribute_values = models.ManyToManyField(ProductAttributeValue, related_name='variant_combinations')
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_variants/', blank=True, null=True)

    def __str__(self):
        attributes = ", ".join([str(value) for value in self.attribute_values.all()])
        return f"{self.product.name} - {attributes}"
    
    def get_final_price(self):
        """
        Calculate the final price after applying the discount.
        """
        if self.discount_percentage:
            final_price = self.price * (1 - (self.discount_percentage / 100))
            return round(final_price, 2)
        return self.price

    def clean(self):
        if self.stock < 0:
            raise ValidationError("Stock cannot be negative")
        if ProductVariantCombination.objects.filter(
            product=self.product,
            attribute_values__in=self.attribute_values.all()
        ).exclude(id=self.id).exists():
            raise ValidationError("This combination of attribute values already exists for this product.")


# Product Image Model
class ProductImage(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    product_variant = models.ForeignKey(ProductVariantCombination, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"
