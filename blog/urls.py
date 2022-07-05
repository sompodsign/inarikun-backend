from django.urls import path

from .views import ArticleDetailView, ArticleListView


urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('<str:pk>/', ArticleDetailView.as_view(), name='article-detail'),

]
