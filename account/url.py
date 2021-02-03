from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path, include
# from django.conf.urls import url
from .views import ChangePasswordView

from account import views

app_name = 'account'
urlpatterns = [
    path('register', views.registration_api),
    # django rest api add default obtain_auth_toke for login
    path('login', obtain_auth_token, name='api_token_auth'),  # <-- And here
    # url(r'^/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('account_view', views.account_view),
    path('update_account_view', views.update_account_view),

]
