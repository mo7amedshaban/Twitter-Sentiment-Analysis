from django.contrib import admin
from django.urls import path, include
from django.urls import re_path

from store.views import IndexTemplateView
from tweets import views

urlpatterns = [
    path('search_tweets', views.get_tweets),
    path('admin/', admin.site.urls),
    path('api/account/', include('account.url')),
    path('api/', include('store.url')),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point"),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
