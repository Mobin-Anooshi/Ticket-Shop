from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView






app_name='accounts'
urlpatterns =[
    path('register/',views.UserRegisterView.as_view(),name='user_register'),
    path('register_driver/',views.UserRegisterDriverView.as_view(),name='driver_register'),
    path('complete_driver/',views.DriverCompleteRegister.as_view(),name='driver_complete'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]