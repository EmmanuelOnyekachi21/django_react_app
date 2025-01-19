from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='public_id'
    )
    liked = serializers.SerializerMethodField()
    liked_count = serializers.SerializerMethodField()

    def validate_author(self, value):
        if self.context['request'].user != value:
            raise ValidationError("You can't create a post for another user.")
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(representation['author'])
        serializer = UserSerializer(author)
        representation['author'] = serializer.data
        return representation
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        return super().update(instance, validated_data)
    
    def get_liked(self, instance):
        request = self.context.get('request', None)
        
        if request is None or request.user.is_anonymous:
            return False
        return request.user.has_liked(instance)
    
    def get_likes_count(self, instance):
        return instance.liked_by.count()

    class Meta:
        model = Post
        # List all the fields that can be included in a request or a response.
        fields = [
            'id', 'author', 'body', 'edited', 'liked', 'created', 'updated',
            'likes_count'
        ]
        read_only_fields = ['edited']