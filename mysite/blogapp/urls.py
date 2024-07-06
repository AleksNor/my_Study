from django.urls import path

from .views import (
    ArticalesListView,
    ArticleDetailView,
    LatestArticlesFeed,
)

app_name = "blogapp"

urlpatterns = [
    path("articles/", ArticalesListView.as_view(), name="articles"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article"),
    path("articles/latest/feed/", LatestArticlesFeed(), name="articles-feed"),
]