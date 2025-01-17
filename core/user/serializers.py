from rest_framework import serializers
from core.user.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer handles the conversion between the User model and JSON data.
    It provides custom handling for the following fields:
    - `id`: A UUID field, serialized as a hex string, representing the public user ID.
    - `created` and `updated`: DateTime fields that are read-only and reflect
        the timestamps when the user was created and last updated.
    """
    id = serializers.UUIDField(
        source='public_id',
        read_only=True,
        format='hex'
    )
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'bio',
            'avatar', 'email', 'is_active', 'created', 'updated'
        ]
        read_only_true = ['is_active']
        """
        The `Meta` class specifies the following:
        - `model`: Specifies the User model to be serialized.
        - `fields`: Specifies the fields from the User model that should be included in the serialized output.
        - `read_only_fields`: Specifies fields that are read-only, meaning they cannot be modified via the serializer.
        """
