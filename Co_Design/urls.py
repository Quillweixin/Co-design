"""Co_Design URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from myapp import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import include

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},
    name='logout'),
    
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login',views.login_action,name='login'),
    path('register',views.register_action,name='register'),
    path('about',views.about,name='about'),
    path('profile/<int:profile_id>',views.profile,name='profile'),
    path('tasks',views.tasks,name='tasks'),
    path('details/<int:id>',views.details, name='details'),
    path('oauth_login',views.oauth_login,name='oauth_login'),
    path('post_request',views.post_request,name='post_request'),
    path('get_avatar/<int:id>',views.get_avatar,name='get_avatar'),
    path('task_image/<int:id>',views.task_image,name='task_image'),
    path('accpet_task',views.accept_task,name='accept_task'),
    path('work',views.work,name='work'),
    path('work_image/<int:id>',views.work_image,name='work_image'),
    path('review/<int:id>',views.review,name='review'),
]
