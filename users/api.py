from django.contrib.auth.models import Permission, Group
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUsers


class UsuariosPermisos(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @staticmethod
    def post(request):
        #if request.user.is_superuser:
        usuario = CustomUsers.objects.get(pk=request.data['usuario'])
        usuario.user_permissions.through.objects.filter(customusers=usuario).delete()
        for a in request.data['permisos']:
            permiso = Permission.objects.get(pk=a)
            usuario.user_permissions.add(permiso)
        usuario.save()
        return Response(status=status.HTTP_201_CREATED)
        #else:
            # return Response(status=status.HTTP_401_UNAUTHORIZED)


class GruposPermisos(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @staticmethod
    def post(request):
        #if request.user.is_superuser:
        grupo = Group.objects.get(pk=request.data['usuario'])
        grupo.permissions.through.objects.filter(group=grupo).delete()
        for a in request.data['permisos']:
            permiso = Permission.objects.get(pk=a)
            grupo.permissions.add(permiso)
        grupo.save()
        return Response(status=status.HTTP_201_CREATED)
        #else:
        #    return Response(status=status.HTTP_401_UNAUTHORIZED)


class GruposUsuarios(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @staticmethod
    def post(request):
        #if request.user.is_superuser:
        grupo = Group.objects.get(pk=request.data['grupo'])
        CustomUsers.groups.through.objects.filter(group=grupo).delete()
        for a in request.data['usuarios']:
            usuario = CustomUsers.objects.get(pk=a)
            usuario.groups.add(grupo)
            usuario.save()
        return Response(status=status.HTTP_201_CREATED)
        #else:
        #    return Response(status=status.HTTP_401_UNAUTHORIZED)
