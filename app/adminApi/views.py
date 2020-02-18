from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication, \
                                BasicAuthentication, SessionAuthentication

from rest_framework.permissions import IsAuthenticated, BasePermission, \
                                        IsAdminUser

from users import serializers
from core.models import User
# Create your views here.


class AdminAuthenticationPermission(BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [BasicAuthentication,
                               SessionAuthentication
                            ]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES)
        return False

#
# class BasicAdminViewset(viewsets.GenericViewSet,
#                      mixins.ListModelMixin,
#                      mixins.CreateModelMixin):
class BasicAdminViewset(viewsets.ModelViewSet):

     authentication_classes = (TokenAuthentication,)
     permission_classes = (IsAuthenticated,
        AdminAuthenticationPermission, IsAdminUser)

     def perform_create(self, serializer):
         serializer.save()


class AdminUserViewSets(BasicAdminViewset):

    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.UserDetailSerializer
        return serializers.UserDetailSerializer
