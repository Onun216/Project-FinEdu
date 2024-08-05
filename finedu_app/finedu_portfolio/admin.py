from django.contrib import admin
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from finedu_portfolio.models import (Company, CompanyHolding,
                                     FinancialStatementCategory,
                                     FinancialStatementMetric, MyPortfolio)


@admin.register(MyPortfolio)
class MyPortfolioAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'name',
    search_fields = 'id', 'name',
    list_per_page = 25
    ordering = '-id',


@admin.register(CompanyHolding)
class CompanyHoldingAdmin(admin.ModelAdmin):
    list_display = 'id', 'company', 'portfolio', 'number_of_shares', 'price_paid_per_share',
    list_display_links = 'company',
    search_fields = 'id', 'company',
    list_per_page = 25
    ordering = 'company',


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'name', 'ticker', 'is_published'
    list_display_links = 'name',
    search_fields = 'id', 'name', 'ticker'
    list_per_page = 25
    ordering = 'name',

    prepopulated_fields = {
        "slug": ('ticker',),
    }
    # autocomplete_fields = '', '',

    def link(self, obj):
        if not obj.pk:
            return '-'

        company_url = obj.get_absolute_url()
        safe_link = mark_safe(
            f'<a target="_blank" href="{company_url}">Ver empresa</a>'
        )

        return safe_link

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user  # type: ignore
        else:
            obj.created_by = request.user  # type: ignore

        obj.save()


@admin.register(FinancialStatementMetric)
class FinancialStatementMetricAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'category',
    list_display_links = 'name',
    search_fields = 'id', 'name',
    list_per_page = 20
    ordering = 'name',


@admin.register(FinancialStatementCategory)
class FinancialStatementCategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'name',
    search_fields = 'id', 'name',
    list_per_page = 10
    ordering = 'name',
