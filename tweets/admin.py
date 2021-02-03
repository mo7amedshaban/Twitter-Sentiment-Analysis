from django.contrib import admin

# Register your models here.
from tweets.models import Tweets

admin.site.register(Tweets)
