from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if permissions.IsAuthenticated().has_object_permission(request, view, obj):
            return obj.author == request.user

        # Instance must have an attribute named `owner`.
        return False


class IsUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        if permissions.IsAuthenticated().has_permission(request, view):
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if permissions.IsAuthenticated().has_object_permission(request, view, obj):
            return obj == request.user

        # Instance must have an attribute named `owner`.
        return False


class IsOwnerCommentOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return True

        if permissions.IsAdminUser().has_permission(request, view):
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if permissions.IsAdminUser().has_object_permission(request, view, obj):
            return True

        # Instance must have an attribute named `owner`.
        return False
