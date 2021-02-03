from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):  # media_cdn
    return 'profile_images/' + str(self.pk) + '/profile_image.png'
    # ------->  self.pk  ==> user number or id of user <-------------


def get_default_profile_image():  # media_cdn
    return "default_image/logo_1080_1080.png"


class Account(AbstractBaseUser):  # here for api      in form use UserCreationForm
    class Meta:
        verbose_name_plural = "Accounts"

    # not use filed for password becouse inherite from AbstractBaseUser  it exist password in it
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                              default=get_default_profile_image)
    age = models.IntegerField(null=True, blank=True)
    phone = models.IntegerField(max_length=12, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'  # when use username in postman set it username and REQUIRED_FIELDS = ['email']
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()  # use it for login

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


# settings.AUTH_USER_MODEL
@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # when after login or register create token in table token
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


