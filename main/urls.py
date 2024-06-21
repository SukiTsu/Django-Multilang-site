from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('question', views.question, name='question'),
    path('blog/<str:ln>/article/<str:inTitle>/', views.article, name="article"),
    path('blog/<str:ln>/<str:message>/', views.error404, name="error"),
    path('article/<str:inTitle>/', views.article, name="article"),
    path('blog/',views.blog, name='blog'),
    path('blog/<str:ln>/', views.blog, name='blog-ln'),
    path('<str:ln>/', views.blog, name='blog'),
    path('', views.home, name='home')
]

urlpatterns += staticfiles_urlpatterns()