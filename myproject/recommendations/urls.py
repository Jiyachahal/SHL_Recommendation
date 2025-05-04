from django.contrib import admin
from django.urls import path
from recommendations import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'), 
    path('api/recommend/', views.api_recommend, name='api_recommend'),

    
]
