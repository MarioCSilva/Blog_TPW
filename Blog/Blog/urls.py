"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', views.main_page,name="home"),
    path('profile/',views.profile_page,name="profile"),
    path('login/', views.entry_page, name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login/'), name='logout'),
=======
    path('index/', views.index),
    path('main_page/', views.main_page),
    path('',views.entry_page),
    path('profile/',views.profile_page),
    path('page/',views.page),
>>>>>>> 212bf5ca045cd3252043e3d20595aca9ad1ebb36
]
