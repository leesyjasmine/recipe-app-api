from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save new user"""
        # 1) Can access the model that the manager is for
        # by just typing self.model;
        # same as creating new user model and assigning to user variable
        if not email:
            raise ValueError('Users must have an email address')
        # 2) self.normalize_email => normalize the email address
        # by lowercasing the domain part
        user = self.model(email=self.normalize_email(email), **extra_fields)
        """Password need encryption so need specific api"""
        user.set_password(password)
        """Required for supporting multiple db"""
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """Creates and save a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Extend User from AbstractBaseUser and PermissionsMixin"""
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
