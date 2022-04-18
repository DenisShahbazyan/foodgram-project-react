from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrIsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthenticatedOrReadOnlyOrIsMe(BasePermission):
    def has_permission(self, request, view):
        return bool(not (view.action == 'me' and request.user.is_anonymous))
