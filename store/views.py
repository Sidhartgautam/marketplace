from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Store
from .serializers import StoreSerializer
from core.utils.pagination import CustomPageNumberPagination
from core.utils.response import PrepareResponse

class StoreCreateView(generics.GenericAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            store = serializer.save()
            response = PrepareResponse(
                success=True,
                data=serializer.data,
                message="Store created successfully"
            )
            return response.send(201)
        response = PrepareResponse(
            success=False,
            data=serializer.errors,
            message="Store creation failed"
        )
        return response.send(400)

class StoreListView(generics.GenericAPIView):
    serializer_class = StoreSerializer
    pagination_class = CustomPageNumberPagination
    def get(self, request, *args, **kwargs):
        country_code = request.GET.get('country_code')
        is_verified = request.GET.get('is_verified', None)
        queryset = Store.objects.all()

        if country_code:
            queryset = queryset.filter(country__code=country_code)
        if is_verified is not None:
            queryset = queryset.filter(is_verified=is_verified.lower() == 'true')

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer.data)

        result = paginated_data['results']
        del paginated_data['results']

        response = PrepareResponse(
            success=True,
            message="Stores fetched successfully",
            data=result,
            meta=paginated_data
        )
        return response.send(200)
