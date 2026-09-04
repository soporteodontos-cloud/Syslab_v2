from rest_framework.serializers import ModelSerializer

from users.models import CustomUsers


class CustomUsersModelSerializer(ModelSerializer):

	class Meta:
		model = CustomUsers
		fields = ['id', 'username']
