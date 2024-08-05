from django.contrib import admin
from django.urls import path
from finedu_portfolio.views import (my_portfolio, my_portfolio_dividends,
                                    my_portfolio_map)

urlpatterns = [
    path('my-portfolio/', my_portfolio, name='my-portfolio'),
    path('my-portfolio-dividends/', my_portfolio_dividends,
         name='my-portfolio-dividends'),
    path('my-portfolio-map/', my_portfolio_map, name='my-portfolio-map'),

]
