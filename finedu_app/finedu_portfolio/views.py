"""
Python Folium
Python Reportlab

"""
import io
import json
import os
from functools import partial
from typing import Any, Dict

import folium
import seaborn
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, TemplateView
from finedu_portfolio.company_info import (current_positions_details,
                                           get_current_positions, locations)
from finedu_portfolio.dividends_positions import (
    div_and_pos, dividend_data_graph, dividends_per_position,
    get_dividends_growth, get_previous_portfolio_positions)
from finedu_portfolio.financial_info import get_financial_info
from finedu_portfolio.forms import FinancialInfoForm
from finedu_portfolio.models import (Company, CompanyHolding,
                                     CompanyHoldingManager,
                                     FinancialStatementCategory,
                                     FinancialStatementMetric, MyPortfolio)
from finedu_portfolio.pdf_config import generate_portfolio_pdf


def my_portfolio_map(request):
    """Portfolio Map"""
    companies = get_current_positions()
    details = current_positions_details
    companies_locations = locations(details)
    latitudes = [float(x) for x in companies_locations[0]]
    longitudes = [float(x) for x in companies_locations[1]]

    # Create a base map centered around a specific location (optional)
    map = folium.Map(location=[40.7128, -74.0059], zoom_start=4)  # NY

    for i, (latitude, longitude) in enumerate(zip(latitudes, longitudes)):
        company_name = companies[i]
        folium.Marker([latitude, longitude], popup=company_name).add_to(map)
        folium.LayerControl().add_to(map)

    # Save the map only if it's newly generated (optional)
    if not os.path.exists('finedu_portfolio/templates/finedu_portfolio/pages/my_portfolio_map.html'):
        map.save(
            'finedu_portfolio/templates/finedu_portfolio/pages/my_portfolio_map.html')
    else:
        print('Mapa já existe')

    return render(request, 'finedu_portfolio/pages/my_portfolio_map.html',
                  context={'map': map})


def my_portfolio(request):
    if request.method == "POST":
        form = FinancialInfoForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data["company"]
            metric = form.cleaned_data["metric"]
            metric_name = metric.name
            # category_id = metric.category_id
            # category_description = metric.category.description
            category_name = metric.category.name
            ticker = company.ticker
            # print(f"Metric: {metric}, Category ID: {category_id}, Name: {category_name}")
            timeline, financial_info = get_financial_info(ticker=ticker,
                                                          category=category_name,
                                                          metric=metric_name)
            # Generate PDF report with timeline and financial info
            pdf_buffer = generate_portfolio_pdf(
                company, metric_name, timeline, financial_info,
                filename=f'{metric_name} - {company.ticker}.pdf')

            response = FileResponse(pdf_buffer, as_attachment=True)
            response['Content-Disposition'] = f'filename={metric_name} - {company.ticker}.pdf'
            return response

        else:
            print(form.errors)
            timeline = None
            financial_info = None
    else:
        form = FinancialInfoForm()
        timeline = None
        financial_info = None
        portfolio = MyPortfolio.objects.all()
        companies = Company.objects.all()
        holdings = CompanyHolding.objects.group_by_company()
        total_nr_shares = CompanyHolding.objects.sum_shares()

    return render(request, "finedu_portfolio/pages/my_portfolio.html",
                  {"form": form, "timeline": timeline,
                   "financial_info": financial_info,
                   "portfolio": portfolio, "companies": companies,
                   "holdings": holdings,
                   "total_nr_shares": total_nr_shares})


def my_portfolio_dividends(request):
    x_dividend_graph, y_dividend_graph = dividend_data_graph()
    yoy_growth_chart_data = get_dividends_growth()
    current_portfolio = get_current_positions()
    previous_portfolio_positions = get_previous_portfolio_positions()

    current_portfolio_dividend_data = []
    for company in sorted(current_portfolio):
        dividends = dividends_per_position(
            div_and_pos, company=company)
        current_portfolio_dividend_data.append(dividends)

    previous_portfolio_dividend_data = []
    for company in sorted(previous_portfolio_positions):
        dividends = dividends_per_position(
            div_and_pos, company=company)
        previous_portfolio_dividend_data.append(dividends)

    return render(request,
                  "finedu_portfolio/pages/my_portfolio_dividends.html",
                  {"current_portfolio_dividend_data": current_portfolio_dividend_data,
                   "previous_portfolio_dividend_data": previous_portfolio_dividend_data,
                   "x_dividend_graph": x_dividend_graph,
                   "y_dividend_graph": y_dividend_graph,
                   "yoy_growth_chart_data": yoy_growth_chart_data})
