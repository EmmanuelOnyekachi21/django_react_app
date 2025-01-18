"""
For the following endpoint, we'll only be allowing the POST and GET methods. This will help us have
the basic features working first.
The code should follow these rules:
• Only authenticated users can create posts
• Only authenticated users can read posts
• Only GET and POST methods are allowed
"""
from rest_framework.permissions import IsAuthenticated
from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status


class PostViewSet(AbstractViewSet):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.all()
    
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
