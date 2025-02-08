from rest_framework import permissions

class IsAdminOrSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  
            return True  # GET, HEAD, OPTIONS sallittu kaikille
        return request.user and (request.user.is_staff or request.user.is_superuser)  # Vain admin tai superuser
