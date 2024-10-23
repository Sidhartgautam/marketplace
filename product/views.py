from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from store.models import Store
from product.models import Product, ProductVariantCombination,ProductImage
from product.serializers import ProductSerializer, ProductVariantCombinationSerializer, ProductImageSerializer
from core.utils.pagination import CustomPageNumberPagination
from core.utils.response import PrepareResponse

# Product Create View
class ProductCreateView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        store_id = self.kwargs.get('store_id')
        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Store not found"
            )
            return response.send(404)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(store=store)
            response = PrepareResponse(
                success=True,
                data=serializer.data,
                message="Product created successfully"
            )
            return response.send(201)
        response = PrepareResponse(
            success=False,
            data=serializer.errors,
            message="Product creation failed"
        )
        return response.send(400)


# Product List View
class ProductListView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination
    # permission_classes = [IsAuthenticated]  # Uncomment if restricted access is needed

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        store_id = request.GET.get('store_id')
        queryset = Product.objects.all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if store_id:
            queryset = queryset.filter(store_id=store_id)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer.data)

        result = paginated_data['results']
        del paginated_data['results']

        response = PrepareResponse(
            success=True,
            message="Products fetched successfully",
            data=result,
            meta=paginated_data
        )
        return response.send(200)


# Product Variant Combination List View
class ProductVariantCombinationListView(generics.GenericAPIView):
    serializer_class = ProductVariantCombinationSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        queryset = ProductVariantCombination.objects.all()

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer.data)

        result = paginated_data['results']
        del paginated_data['results']

        response = PrepareResponse(
            success=True,
            message="Product variants fetched successfully",
            data=result,
            meta=paginated_data
        )
        return response.send(200)
    
class ProductImageCreateView(generics.GenericAPIView):
    serializer_class = ProductImageSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, product_id, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Product not found",
            )
            return response.send(404)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            response = PrepareResponse(
                success=True,
                data=serializer.data,
                message="Image added successfully"
            )
            return response.send(201)
        response = PrepareResponse(
            success=False,
            data=serializer.errors,
            message="Failed to add image"
        )
        return response.send(400)


# Product Image List View
class ProductImageListView(generics.GenericAPIView):
    serializer_class = ProductImageSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Product not found",
            )
            return response.send(404)

        queryset = ProductImage.objects.filter(product=product)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer.data)

        result = paginated_data['results']
        del paginated_data['results']

        response = PrepareResponse(
            success=True,
            message="Product images fetched successfully",
            data=result,
            meta=paginated_data
        )
        return response.send(200)
