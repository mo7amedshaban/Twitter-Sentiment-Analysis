from django.shortcuts import render

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer
from rest_framework import generics

from account.serializers import AccountSerializer, UpdateAccountSerializer, UserLoginSerializer

from rest_framework import status
from .models import Account


@api_view(['POST', ])
@permission_classes([~IsAuthenticated])
def registration_api(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST', ])
@permission_classes([~IsAuthenticated])
def login_api(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = Account.objects.get(email=request.data["username"])

            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)





    #     serializer = UserLoginSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response(serializer.errors)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def account_view(request):
    try:
        account = request.user  # Account.objects.get(pk=1)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountSerializer(account)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = UpdateAccountSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save(image=request.data.get('image'))
            data['response'] = 'Account update success'

            return Response(data=data)
        return Response(serializer.errors)


# class AccountRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UpdateAccountSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         serializer = self.serializer_class(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def update(self, request, *args, **kwargs):
#         serializer = self.serializer_class(request.user, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = Account

    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]})
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': [],
            }

            return Response(response)

        return Response(serializer.errors)
