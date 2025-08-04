from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        return request.user.is_authenticated and request.user.is_superuser
