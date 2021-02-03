from django.db import models


# Create your models here.
class Tweets(models.Model):
    class Meta:
        verbose_name = "Tweets"
        verbose_name_plural = "Tweets"

    def __str__(self):
        pass
