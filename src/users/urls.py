from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('update/', views.ChangeUser.as_view(), name='change'),
]
