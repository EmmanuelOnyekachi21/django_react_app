from django.db import models
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from core.abstract.models import AbstractManager, AbstractModel


class UserManager(BaseUserManager, AbstractManager):
    """
    Custom manager for User model. This manager provides helper methods
    to create regular users and superusers.
    """
    def create_user(self, username, email, password=None, **kwargs):
        """
        Create and return a regular user with an email, username, 
        and password.
        
        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            **kwargs: Additional fields for user creation.
        
        Raises:
            TypeError: If username, email, or password is None.
        
        Returns:
            User: The created User instance.
        """
        if username is None:
            raise TypeError("User must have a username.")
        if email is None:
            raise TypeError("User must have an email.")
        if password is None:
            raise TypeError('Password can\'t be empty')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **kwargs):
        """
        Create and return a User with superuser permissions.
        
        Args:
            username (str): The username of the superuser.
            email (str): The email address of the superuser.
            password (str, optional): The password for the superuser. Defaults to None.
            **kwargs: Additional fields for user creation.
        
        Raises:
            TypeError: If username, email, or password is None.
        
        Returns:
            User: The created superuser instance.
        """
        if password is None:
            raise TypeError("SuperUsers must have a password")
        if username is None:
            raise TypeError("SuperUser must have a username.")
        if email is None:
            raise TypeError("SuperUser must have an email.")

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin, AbstractModel):
    """
    Custom User model that extends AbstractBaseUser and PermissionsMixin 
    to allow authentication and authorization functionality, along with custom fields.
    """
    username = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    bio = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to="img", blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    
    def __str__(self):
        """
        String representation of the User model. Returns the user's email address.
        
        Returns:
            str: The user's email address.
        """
        return f"{self.email}"
    
    @property
    def name(self):
        """
        Property that returns the user's full name by combining the first name 
        and last name fields.
        
        Returns:
            str: The user's full name (first name + last name).
        """
        return f"{self.first_name} {self.last_name}"

