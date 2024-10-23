from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer
from product.models import ProductVariantCombination
from core.utils.response import PrepareResponse

# Get details of the active cart for the authenticated user
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        response = PrepareResponse(
            success=True,
            data=serializer.data,
            message="Cart details fetched successfully"
        )
        return response.send(code=200)


# Add or update a cart item
class CartItemAddView(generics.GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        data = request.data.copy()
        data['cart'] = cart.id
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            product_variant = serializer.validated_data['product_variant']
            quantity = serializer.validated_data['quantity']

            # Check if the item already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product_variant=product_variant,
                defaults={'quantity': quantity}
            )

            if not created:
                # Update quantity if the item is already in the cart
                cart_item.quantity += quantity
                if cart_item.quantity > product_variant.stock:
                    response = PrepareResponse(
                        success=False,
                        message="Not enough stock available."
                    )
                    return response.send(code=400)
                cart_item.save()

            response = PrepareResponse(
                success=True,
                data=CartSerializer(cart).data,
                message="Item added to cart successfully"
            )
            return response.send(code=201)
        
        response = PrepareResponse(
            success=False,
            data=serializer.errors,
            message="Failed to add item to cart"
        )
        return response.send(code=400)


# Update or delete a cart item
class CartItemUpdateView(generics.GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user, cart__is_active=True)
        except CartItem.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Cart item not found."
            )
            return response.send(code=404)
        
        serializer = self.get_serializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = PrepareResponse(
                success=True,
                data=CartSerializer(cart_item.cart).data,
                message="Cart item updated successfully"
            )
            return response.send(code=200)
        
        response = PrepareResponse(
            success=False,
            data=serializer.errors,
            message="Failed to update cart item"
        )
        return response.send(code=400)

    def delete(self, request, cart_item_id, *args, **kwargs):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user, cart__is_active=True)
        except CartItem.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Cart item not found."
            )
            return response.send(code=404)
        
        cart_item.delete()
        response = PrepareResponse(
            success=True,
            message="Cart item removed successfully"
        )
        return response.send(code=204)
