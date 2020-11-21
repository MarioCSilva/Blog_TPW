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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page,name="home"),
    path('profile/',views.profile_page,name="profile"),
    path('login/', views.entry_page, name='login'),
    path('blog/<int:num>', views.blog_page, name='blog'),
    path('logout', auth_views.LogoutView.as_view(next_page='login/'), name='logout'),
    path('my_blog/',views.my_blog),
    path('blog_owners/', views.blog_owners),
    path('blog_topics/', views.blog_topics),
    path('blog_edit/', views.blog_edit),
    path('blog_subs/', views.blog_subs),
    path('blog_follow/', views.blog_follow),
    path('blog_delete/', views.blog_delete),
    path('blog_visibility/', views.blog_visibility),
    path('blog_invites/', views.blog_invites),
    path('blog_post/', views.blog_post),
    path('settings/',views.settings,name="settings"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)