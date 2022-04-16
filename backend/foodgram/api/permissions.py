from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user.is_staff)


class IsAuthorOrIsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or obj.author == request.user
        )