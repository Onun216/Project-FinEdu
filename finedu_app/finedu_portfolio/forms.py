from django import forms
from finedu_portfolio.models import (Company, FinancialStatementCategory,
                                     FinancialStatementMetric)


class FinancialInfoForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all())
    metric = forms.ModelChoiceField(
        queryset=FinancialStatementMetric.objects.all())
