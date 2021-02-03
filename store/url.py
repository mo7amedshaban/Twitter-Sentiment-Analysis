from rest_framework.authtoken.views import obtain_auth_token

from store import views
# from store.views import ProductListApi
from store.views import ProductListApi
from django.urls import path, include

urlpatterns = [
    # -------> class Based Views  <-----------
    # pagination
    path('list', ProductListApi.as_view(), name="list"),
    # path('<str:slug>', ProductListApi.as_view()),

    # -------> Functions Based Views  <-----------
    path('<str:slug>', views.list_api),
    path('update/<str:slug>', views.update_api),
    path('post', views.post_api),
    path('delete/<str:slug>', views.delete_api),


]
