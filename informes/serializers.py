from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import Serializer


class trabajosPorAreaSerializer(Serializer):
	area = CharField()
	cantidad = IntegerField()