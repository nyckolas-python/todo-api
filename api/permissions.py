from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    """Is the owner of the task"""

    message = "You don't have permission to access"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if obj.user == request.user:
            return True
        # Instance must have an attribute named `user`.
        return False


class IsExecutor(permissions.IsAuthenticated):
    """Is the executor of the task"""

    message = "You don't have permission to access"
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        if request.user in obj.executors.all():
            return True
        
        return False