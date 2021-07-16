from django.urls import path

from . import views

urlpatterns = [
  path('', views.register, name='register'), # our-domain.com
  path('<str:user_id>', views.index, name='index'), # our-domain.com

]