from django.urls import path

from . import views

urlpatterns = [
  path('', views.register, name='register'), # our-domain.com
  path('login', views.login, name='login'),
  path('<str:user_id>/calculate', views.calculate, name='calculate'),
  path('<str:user_id>', views.index, name='index'), # our-domain.com
  
  

]