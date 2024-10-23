from django.shortcuts import render

# Create your views here.
# wishlist/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from wishlist.models import Wishlist, WishlistItem
from wishlist.serializers import WishlistSerializer, WishlistItemSerializer
from core.utils.response import PrepareResponse
from product.models import Product

class WishlistDetailView(generics.RetrieveAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        return wishlist

    def get(self, request, *args, **kwargs):
        wishlist = self.get_object()
        serializer = self.get_serializer(wishlist)
        response = PrepareResponse(
            success=True,
            data=serializer.data,
            message="Wishlist fetched successfully"
        )
        return response.send(status.HTTP_200_OK)


class WishlistItemAddView(generics.GenericAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        data = request.data.copy()
        data['wishlist'] = wishlist.id
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            product = serializer.validated_data['product']

            # Check if the product is already in the wishlist
            if WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
                response = PrepareResponse(
                    success=False,
                    message="Product is already in the wishlist."
                )
                return response.send(code=200)

            serializer.save(wishlist=wishlist)
            response = PrepareResponse(
                success=True,
                data=serializer.data,
                message="Product added to wishlist successfully"
            )
            return response.send(code=201)
        
        response = PrepareResponse(
            success=False,
            data=serializer.errors,
            message="Failed to add product to wishlist"
        )
        return response.send(code=400)


class WishlistItemRemoveView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WishlistItem.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            wishlist_item = WishlistItem.objects.get(id=kwargs['pk'], wishlist__user=request.user)
            wishlist_item.delete()
            response = PrepareResponse(
                success=True,
                message="Product removed from wishlist successfully"
            )
            return response.send(code=204)
        except WishlistItem.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Item not found in your wishlist"
            )
            return response.send(code=404)
