from django.urls import path, include
from rest_framework.routers import SimpleRouter
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import logout, ActivateUserViewSet, GetUserDataView, \
    UserViewSet, SignUpView, TokenCreateView

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
                  path('register/', SignUpView.as_view({
                      'post': 'create'
                  }), name='register'),
                  path('userdata/', GetUserDataView.as_view(), name='userdata'),
                  path('logout/', logout, name='logout'),
                  path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('create-token/', TokenCreateView.as_view({
                      'post': 'create'
                  }), name='create-token'),
                  path('activate-account/<uidb64>/<token>/', ActivateUserViewSet.as_view({
                      'get': 'activate'
                  }),
                       name='activate'),

              ] + router.urls
