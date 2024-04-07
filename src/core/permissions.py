from rest_framework.permissions import BasePermission, SAFE_METHODS

from organizations.repositories import OrganizationRepository


class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class IsOrganizationOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == OrganizationRepository.get(request.kwargs.get('id'))
