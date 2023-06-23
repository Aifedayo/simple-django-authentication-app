from django.urls import path

from .views import (LogInView)


app_name = 'accounts'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
]
