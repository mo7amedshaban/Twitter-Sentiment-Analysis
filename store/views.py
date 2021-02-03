from django.shortcuts import render

from rest_framework import authentication, generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter


@api_view(['GET', ])
def list_api(request, slug):
    try:
        products = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(products)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
def update_api(request, slug):
    try:
        products = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # here not any user make edit but user posted it only
    user = request.user
    if products.account != user:
        return Response({'you are not post this post for make edit but only who poster'})

    if request.method == "PUT":
        serializer = ProductSerializer(products, data=request.data)
        if serializer.is_valid():
            # edit on serializer fields
            serializer.validated_data['category_id'] = 1
            serializer.validated_data['title'] = 'yes'

            serializer.save()  # serializer.save(title='yes')
            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def post_api(request):
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_api(request, slug):
    try:
        products = Product.objects.get(slug=slug)
    except products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {}
    if request.method == 'DELETE':
        products.delete()
        data['Delete'] = 'successfully'
        return Response(data=data, status=status.HTTP_200_OK)


class ProductListApi(generics.ListAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = (TokenAuthentication,)  # must use ,
    permission_classes = (IsAuthenticated,)  # must all ,
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'slug', 'account__username']  # when use relationship
    ordering_fields = ['title']















class IndexTemplateView(TemplateView):
    def get_template_names(self):
        template_name = "index.html"
        return template_name

#
# class ProductListApi(generics.ListAPIView):
#     model = Product
#     # queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get_queryset(self):
#         ok = Product.objects.all()
#         return ok
#
#
# def category():
#     pass
