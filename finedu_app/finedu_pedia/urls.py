"""
from django.urls import path
from . import views

app_name = 'finedu_pedia'


urlpatterns = [
    path('glossary-home/', views.glossary_home, name='glossary-home'),
    path('members/', views.members, name='members'),
]
"""

from django.urls import path
from finedu_pedia.views import (GlossaryItemListView, GlossaryItemDetailView, 
                                GlossaryPageDetailView, CreatedByListView,
                                SearchListView)


app_name = 'finedu_pedia'


urlpatterns = [
        path('glossary-home/', GlossaryItemListView.as_view(), 
             name='glossary-home'),
        path('glossary-item/<slug:slug>/', GlossaryItemDetailView.as_view(), 
             name='glossary-item'),
        path('glossary-page/<slug:slug>/', GlossaryPageDetailView.as_view(), 
             name='glossary-page'),
        path('created_by/<int:author_pk>/', CreatedByListView.as_view(),
             name='created_by'
            ),
        path('glossary-search/', SearchListView.as_view(), 
             name='glossary-search'),
]
