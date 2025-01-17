from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from core.user.models import User
from core.user.serializers import UserSerializer
from core.abstract.viewsets import AbstractViewSet


class UserViewSet(AbstractViewSet):
    """
    A viewset for managing User objects.
    
    This viewset provides restricted access to user-related actions, allowing
    authenticated users to retrieve and partially update user data. Superusers
    have access to all user data, while non-superusers are restricted from 
    accessing superuser accounts.
    """
    http_method_names = ('patch', 'get')
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Return the appropriate queryset based on the requesting user's permissions.
        
        - Superusers: Can view all users.
        - Non-superusers: Can view all users except superusers.
        
        Returns:
            QuerySet: A filtered queryset of User objects.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.all().exclude(is_superuser=True)
    
    def get_object(self):
        """
        Retrieve and return a single User object identified by the public ID.

        Ensures that the requesting user has the necessary permissions to access 
        the object.

        Returns:
            User: The requested User object.

        Raises:
            PermissionDenied: If the user lacks the necessary permissions.
        """
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
