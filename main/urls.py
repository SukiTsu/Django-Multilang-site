from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('question/<str:ln>/', views.question, name='question'),
    path('blog/<str:ln>/article/<str:inId>/', views.article, name="article"),
    path('article/<str:inId>/', views.article, name="article"),
    path('blog/',views.blog, name='blog'),
    path('blog/<str:ln>/', views.blog, name='blog-ln'),
    path('', views.home, name='home')
]

urlpatterns += staticfiles_urlpatterns()