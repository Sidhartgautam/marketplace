# coupons/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from coupons.models import Coupon
from coupons.serializers import CouponSerializer
from core.utils.response import PrepareResponse

class ApplyCouponView(generics.GenericAPIView):
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        cart_total = request.data.get('cart_total')

        if not code or cart_total is None:
            response = PrepareResponse(
                success=False,
                message="Code and cart_total are required."
            )
            return response.send(code=400)

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            response = PrepareResponse(
                success=False,
                message="Invalid coupon code."
            )
            return response.send(code=404)

        try:
            cart_total = float(cart_total)
        except ValueError:
            response = PrepareResponse(
                success=False,
                message="Invalid cart_total value. It must be a number."
            )
            return response.send(code=400)

        final_price, discount, message = coupon.apply_coupon(request.user, cart_total)

        response = PrepareResponse(
            success=True if discount > 0 else False,
            message=message,
            data={
                "final_price": final_price,
                "discount": discount,
                "original_price": cart_total
            }
        )
        return response.send(code=200 if discount > 0 else 400)
