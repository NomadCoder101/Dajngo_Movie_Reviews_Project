from django.urls import path, re_path,include

from . import views


app_nme = 'news'

urlpatterns =[
    
   path('', views.news, name='news'),

]
