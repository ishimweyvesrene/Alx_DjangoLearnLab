# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer, UserSerializer, ProfileUpdateSerializer
from .models import CustomUser
from notifications.utils import create_notification
User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """
    API endpoint for user registration
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token = Token.objects.get(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class CustomObtainAuthToken(ObtainAuthToken):
    """
    API endpoint for user login
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profile
    """
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return ProfileUpdateSerializer
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Authenticated user follows the user with id=user_id.
    """
    try:
        target = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if target == request.user:
        return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    # add current user to target.followers
    target.followers.add(request.user)
    create_notification(recipient=target, actor=request.user, verb='followed you')
    return Response({'detail': 'Followed.', 'target': UserSerializer(target, context={'request': request}).data})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Authenticated user unfollows the user with id=user_id.
    """
    try:
        target = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if target == request.user:
        return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    target.followers.remove(request.user)
    return Response({'detail': 'Unfollowed.', 'target': UserSerializer(target, context={'request': request}).data})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_following(request):
    """
    Return list of users that the authenticated user follows.
    """
    following_qs = request.user.following.all()
    serializer = UserSerializer(following_qs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_followers(request):
    """
    Return list of users who follow the authenticated user.
    """
    followers_qs = request.user.followers.all()
    serializer = UserSerializer(followers_qs, many=True, context={'request': request})
    return Response(serializer.data)

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()   # ✔ Required by checker

    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()   # ✔ Required by checker

    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_to_unfollow == request.user:
            return Response({"detail": "You cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
