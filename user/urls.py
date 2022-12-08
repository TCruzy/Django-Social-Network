from django.urls import path, include
from rest_framework.routers import SimpleRouter
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import UserCreateView, logout, ActivateUserViewSet, CustomTokenObtainPairView, GetUserDataView, \
    UserViewSet

router = SimpleRouter()
router.register('', UserViewSet, basename='user')
router.register('activate-user/(?P<uid>[^/.]+)/(?P<token>[^/.]+)', ActivateUserViewSet, basename='activate-user')

urlpatterns = [
                  path('register/', UserCreateView.as_view(), name='register'),
                  path('token-auth/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('userdata/', GetUserDataView.as_view(), name='userdata'),
                  path('logout/', logout, name='logout'),
                  path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

              ]
