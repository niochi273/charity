from .views import (
                    ShowArticle, ArticleList, HomeList,
                    SearchNews, TagArticleList, CategoryArticleList,
                    SuccessfulPurchase, ScrewedupPurchase, DonateView
                    )
from django.urls import path

urlpatterns = [
    path('', HomeList, name="home"),
    path("donate/", DonateView, name="donate"),
    path("donate/success/", SuccessfulPurchase, name="success"),
    path("donate/cancel/", ScrewedupPurchase, name="cancel"),
    path('search/', SearchNews, name="search"),
    path('news/', ArticleList.as_view(), name='all_news'),
    path('tag/<slug:tag_slug>', TagArticleList.as_view(), name='tag'),
    path('category/<slug:category_slug>', CategoryArticleList.as_view(), name='category'),
    path('article/<slug:article_slug>', ShowArticle.as_view(), name='article'),
]