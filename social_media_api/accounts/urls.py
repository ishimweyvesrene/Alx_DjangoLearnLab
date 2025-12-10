# accounts/urls.py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import follow_user, unfollow_user, my_following, my_followers
# Import views using lazy loading to avoid circular imports
def get_register_view():
    from .views import RegisterAPIView
    return RegisterAPIView.as_view()

def get_login_view():
    from .views import CustomObtainAuthToken
    return CustomObtainAuthToken.as_view()

def get_profile_view():
    from .views import ProfileRetrieveUpdateAPIView
    return ProfileRetrieveUpdateAPIView.as_view()

urlpatterns = [
    path('register/', get_register_view(), name='register'),
    path('login/', get_login_view(), name='login'),
    path('profile/', get_profile_view(), name='profile'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('me/following/', my_following, name='my-following'),
    path('me/followers/', my_followers, name='my-followers'),
]
