from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):

    def create_user(self, user_name, email, birthday, password=None):

        user = self.model(user_name=user_name, email=email, birthday=birthday)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_name, email, birthday, password=None):
        user = self.create_user(
            user_name=user_name,
            email=email,
            password=password,
            birthday=birthday,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['birthday', 'email']

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

