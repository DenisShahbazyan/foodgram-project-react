from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrIsAdminOrReadOnly(BasePermission):
    """Пермишен пускает только Автора или Администратора. Для остальных доступ
    только на чтение.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
        )


class IsAuthenticatedOrReadOnlyOrIsMe(BasePermission):
    """Пермишен пускает по action == 'me' только авторизованных пользователей.
    """

    def has_permission(self, request, view):
        return bool(not (view.action == 'me' and request.user.is_anonymous))
