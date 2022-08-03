from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('signup', views.signup),
                  path('', views.login_user, name='login'),
                  path('Publish_Post/', views.Publish_Post, name='Publish_Post'),
                  path('Publish_Post1/', views.Publish_Post1, name='Publish_Post1'),
                  path('All_Post/', views.All_Post, name='All_Post'),
                  path('blogpost/<int:id>', views.blogpost, name="blogPost"),
                  path('logout/', views.logout_user, name="logout"),
                  path('like_dislike/', views.like_dislike, name="like_dislike"),
              ]

