from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


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


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        # recommended way to retrieve from settings from Django
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # string representation of model
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        # recommended way to retrieve from settings from Django
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # string representation of model
    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # blank is not same as null.;
    # If no value passed, field will set as blank;
    # Udemy recommend use blank instead of null for easier check;
    # because in this case after check null still need check blank;
    # before redirect to link
    link = models.CharField(max_length=255, blank=True)
    # It is possible to put Ingredient as a class
    # instead of 'Ingredient' as a string.
    # However, if put Ingredient as a class, need to sort
    # the class according to dependency so put as string is better
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
