from rest_framework import permissions, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import SAFE_METHODS


class NeedLogin(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'message': 'Permission denied. For this action user must be a superuser.'}
    default_code = 'not_authenticated'


class IsAdminOrReadOnly(permissions.IsAdminUser):
    message = 'This action allowed only for admin.'

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        if is_admin:
            return is_admin

        else:
            if request.method != 'GET':
                raise NeedLogin
            return request.method in SAFE_METHODS
