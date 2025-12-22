from rest_framework import serializers
from todo_app.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    """
    Defines the serialization and deserialization rules for Todo model instances.
    """

    class Meta:
        """
        Specifies the model binding and field inclusion configuration for the serializer.
        """
        model = Todo
        fields = '__all__'
