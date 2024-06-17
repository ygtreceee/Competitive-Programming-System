"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

urlpatterns = [
    # path('admin/', admin.site.urls),

    # www.xxx.com/index  -> function views.index

    # http://localhost:8000/index

    path('layout', views.layoutPage),

    path('index', views.index),
    path('mylist', views.mylist),

    path('login', views.loginPage),
    path('logout', views.logoutPage),

    path('attend/<int:id>/<str:type>', views.attend),
    path('attendDelete/<int:id>/<str:type>', views.attendDelete),


    path('register', views.registerPage),
    path('<int:nid>/profile', views.profilePage),

    path('ProblemManagement/list', views.Problem_list),
    path('ProblemManagement/add', views.Problem_add),
    path('ProblemManagement/<int:nid>/delete', views.Problem_delete),
    path('ProblemManagement/<int:nid>/edit', views.Problem_edit),

    path('ProblemSet', views.ProblemSetPage),

]
