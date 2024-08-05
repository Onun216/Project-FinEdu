from django.urls import path
from . import views

app_name = 'finedu_home'


urlpatterns = [
    path('home/', views.home, name='home'),
]
    
