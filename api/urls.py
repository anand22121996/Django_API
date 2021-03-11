from django.urls import path
from . import views
from api import views
urlpatterns = [
   path('articles/',views.article_list),
   path('article/<int:pk>/', views.article_detail),
   path('articlec/', views.ArticleAPIView.as_view()),
   path('articlec/<int:id>/', views.ArticleDetail.as_view()),
   path('articlegeneric/', views.LCArticleAPI.as_view()),
   path('articlegeneric/<int:pk>/', views.RUDArticleAPI.as_view()),
]