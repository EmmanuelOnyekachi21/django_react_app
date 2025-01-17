from django.db import models
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        """
        Retrieve a User object by its unique public_id.
        
        Args:
            public_id (UUID): The unique public identifier of the user.
        
        Returns:
            User: The User instance with the specified public_id.
            Http404: If the User is not found, raises an HTTP 404 error.
        """
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class AbstractModel(models.Model):
    public_id = models.UUIDField(
        db_index=True,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AbstractManager()
    
    class Meta:
        abstract = True