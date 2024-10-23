from rest_framework import generics, permissions
from review.models import ProductReview
from review.serializers import ProductReviewSerializer
from product.models import Product
from core.utils.response import PrepareResponse

# Create a review for a product
class ProductReviewCreateView(generics.GenericAPIView):
    serializer_class = ProductReviewSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Product not found"
            )
            return response.send(404)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            response = PrepareResponse(
                success=True,
                data=serializer.data,
                message="Review added successfully"
            )
            return response.send(201)
        response = PrepareResponse(
            success=False,
            data=serializer.errors,
            message="Failed to add review"
        )
        return response.send(400)


# List all reviews for a specific product
class ProductReviewListView(generics.GenericAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Product not found"
            )
            return response.send(404)

        queryset = ProductReview.objects.filter(product=product)
        serializer = self.serializer_class(queryset, many=True)
        
        response = PrepareResponse(
            success=True,
            data=serializer.data,
            message="Product reviews fetched successfully"
        )
        return response.send(200)
