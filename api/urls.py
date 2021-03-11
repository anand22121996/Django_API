from django.urls import path, include
from . import views
from api import views
from rest_framework.routers import DefaultRouter

# creating router object
router = DefaultRouter()
router.register('articlemvs',views.ArticleModelViewSet, basename='article')

urlpatterns = [
   path('articles/',views.article_list),
   path('article/<int:pk>/', views.article_detail),
   path('articlec/', views.ArticleAPIView.as_view()),
   path('articlec/<int:id>/', views.ArticleDetail.as_view()),
   path('articlegeneric/', views.LCArticleAPI.as_view()),
   path('articlegeneric/<int:pk>/', views.RUDArticleAPI.as_view()),
   path('articleapi/', views.LCAPIView.as_view()),
   path('articleapi/<int:pk>',views.RUDAPIView.as_view()),
   path('',include(router.urls)),
]