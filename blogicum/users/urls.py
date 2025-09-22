from django.urls import path
from .views import SignUp

app_name = 'users'

urlpatterns = [
    path('registration/', SignUp.as_view(), name='registration'),
]
