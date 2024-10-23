from rest_framework import serializers
from review.models import ProductReview

class ProductReviewSerializer(serializers.ModelSerializer):
    product=serializers.StringRelatedField()
    full_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class Meta:
        model = ProductReview
        fields = ['id','full_name','user_id', 'rating', 'review_text', 'product']
        read_only_fields = ['id', 'user', 'product']

    def get_full_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.last_name}" if user else "Unknown"
    
    def get_user_id(self, obj):
        user = obj.user
        return user.id if user else None
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value