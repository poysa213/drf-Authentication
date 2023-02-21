from django.urls import re_path, include , path


from knox import views as knox_views
from authentication.views import  LoginView, RegisterView


app_name = 'authentication'

urlpatterns = [
  # re_path(r'api/auth/', include('knox.urls')),
  path('create/',RegisterView.as_view(), name="create"),
  # path('profile/', ManageUserView.as_view(), name='profile'),
  path('login/', LoginView.as_view(), name='knox_login'),
  path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
  path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall') ]
