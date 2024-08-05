from django.urls import path
from finedu_blog.views import (BlogPostListView, BlogPostDetailView,
                               BlogPageDetailView, CreatedByListView,
                               SearchListView)


app_name = 'finedu_blog'


urlpatterns = [
    path('blog-home/', BlogPostListView.as_view(),
         name='blog-home'),
    path('blog-post/<slug:slug>/', BlogPostDetailView.as_view(),
         name='blog-post'),
    path('blog-page/<slug:slug>/', BlogPageDetailView.as_view(),
         name='blog-page'),
    path('created_by/<int:author_pk>/', CreatedByListView.as_view(),
         name='created_by'
         ),
    path('blog-search/', SearchListView.as_view(),
         name='blog-search'),
]
