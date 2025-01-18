from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    """
    Custom Permission to allow different level of acccess based on user type.
    """
    def has_object_permission(self, request, view, obj):
        # Anonymous users can only read (SAFE_METHODS)
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        
        # Authenticated users can interact with objects if authenticated
        if view.basename in ['post']:
            return bool(request.user and request.user.is_authenticated)
        return False
    
    def has_permission(self, request, view):
        # Anonymous users can only read (SAFE_METHODS, i.e GET, OPTION, HEAD )
        if view.basename in ['post']:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS
            
            # Authenticated users can access
            return bool(request.user and request.user.is_authenticated)
        return False