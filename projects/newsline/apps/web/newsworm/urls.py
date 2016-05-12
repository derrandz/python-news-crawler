# Here goes the urls configuration for the newsworm app
from django.conf.urls import url

from .views import general_views

urlpatterns = [
    url(r'^home$', general_views.home, name='home'),
]