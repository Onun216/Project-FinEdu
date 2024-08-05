import json
import time
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from fake_useragent import UserAgent
from finedu_portfolio.access_info import GF_API_TOKEN

# Relevant Metrics for businesses
income_statement = ['Revenue', 'Gross Profit', 'Gross Margin %', 'Selling, General, & Admin. Expense',
                    'Research & Development', 'Total Operating Expense',
                    'Operating Income', 'Operating Margin %', 'Interest Income', 'Interest Expense',
                    'Net Income', 'Net Margin %', 'EPS (Diluted', 'Shares Outstanding (Diluted Average)',
                    'EBITDA', 'Depreciation, Depletion and Amortization']

balance_sheet = ['Cash and Cash Equivalents', 'Cash, Cash Equivalents, Marketable Securities',
                 'Accounts Receivable', 'Total Inventories', 'Total Current Assets',
                 'Gross Property, Plant and Equipment', 'Intangible Assets', 'Goodwill',
                 'Total Long-Term Assets', 'Total Assets', 'Accounts Payable', 'Long-Term Debt',
                 'Long-Term Debt & Capital Lease Obligation', 'Debt-to-Equity',
                 'Pension And Retirement Benefit',
                 'Total Liabilities', 'Preferred Stock', 'Retained Earnings', 'Treasury Stock',
                 'Total Stockholders Equity']

cashflow_statement = ['Change In Inventory', 'Stock Based Compensation', 'Cash Flow from Operations',
                      'Purchase Of Property, Plant, Equipment', 'Sale Of Property, Plant, Equipment',
                      'Purchase Of Business', 'Sale Of Business', 'Purchase Of Investment',
                      'Sale Of Investment',
                      'Issuance of Stock', 'Repurchase of Stock', 'Issuance of Debt', 'Payments of Debt',
                      'Cash Flow from Financing', 'Effect of Exchange Rate Changes', 'Capital Expenditure',
                      'Free Cash Flow']

valuation_ratios = ['PE Ratio', 'Price-to-Owner-Earnings', 'PB Ratio', 'Price-to-Tangible-Book',
                    'Price-to-Free-Cash-Flow', 'Price-to-Operating-Cash-Flow', 'PS Ratio', 'PEG Ratio',
                    'EV-to-Revenue', 'EV-to-EBITDA', 'Dividend Yield %']

per_share_metrics = ['EBIT per Share', 'Earnings per Share (Diluted)', 'Cash per Share', 'Dividends per Share',
                     'Book Value per Share', 'Tangible Book per Share', 'Total Debt per Share']

common_size_ratios = ['ROE %', 'ROA %', 'Return-on-Tangible-Asset', 'ROIC %', 'WACC %',
                      'Effective Interest Rate on Debt %',
                      'Gross Margin %', 'Operating Margin %', 'Net Margin %', 'EBITDA Margin %', 'FCF Margin %',
                      'Debt-to-Equity', 'Inventory Turnover', 'COGS-to-Revenue', 'Inventory-to-Revenue',
                      'Capex-to-Revenue',
                      'Capex-to-Operating-Income', 'Capex-to-Operating-Cash-Flow']

# Convert table into dataframe
table = dict({'per_share_data_array': np.array(per_share_metrics),
              'common_size_ratios': np.array(common_size_ratios),
              'income_statement': np.array(income_statement),
              'balance_sheet': np.array(balance_sheet),
              'cashflow_statement': np.array(cashflow_statement),
              'valuation_ratios': np.array(valuation_ratios)})

df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in table.items()]))

CATEGORIES = (
    ('per_share_data_array', 'Dados por ação'),
    ('common_size_ratios', 'Rácios'),
    ('income_statement', 'Declaração de rendimentos'),
    ('balance_sheet', 'Balanço'),
    ('cashflow_statement', 'Fluxos de caixa'),
    ('valuation_ratios', 'Rácios de avaliação')
)

METRICS_MAP = {
    'per_share_data_array': per_share_metrics,
    'common_size_ratios': common_size_ratios,
    'income_statement': income_statement,
    'balance_sheet': balance_sheet,
    'cashflow_statement': cashflow_statement,
    'valuation_ratios': valuation_ratios
}

# Show available categories and metrics for chosen category
"""
def gf_choose_metric():
    ticker = input('\nInsira um ticker: ')
    print('Categorias disponíveis para pesquisa:')
    for keys in table.keys():
        print(keys)

    cat = input('\nInsira uma categoria: ')
    print('\nMétricas disponíveis para pesquisa: ')
    for metric in table[cat]:
        print(metric)

    metric = input('\nInsira uma métrica: ')
    return ticker, cat, metric
"""


# Use the GuruFocus API to get financial info
# Note: For all stocks that are not traded in the US,
# please replace {symbol} with {exchange:symbol} when calling the api. For example: ASX:ABC
def get_gf_summary():
    """
    Function returns a GuruFocus company summary using GF's API
    For terminal use
    """
    ticker = input('\nInsira um ticker: ')
    url = f'https://api.gurufocus.com/public/user/{GF_API_TOKEN}/stock/{ticker}/summary'

    try:
        # Set a random User-Agent header
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        gf_request = Request(url, headers=headers)

        # Add a delay between requests to avoid rate limits
        time.sleep(2)  # You can adjust the delay time as needed

        gf_info = urlopen(gf_request).read()
        data = json.loads(gf_info.decode('utf8'))
        print(data)

    except Exception as e:
        print(e)


def get_gf_metric():
    """
    Function returns a GuruFocus company financial satement metric using GF's API
    For terminal use only
    """
    print('Categorias disponíveis para pesquisa: ')
    for keys in table.keys():
        print(keys)
    category = input('\nInsira uma categoria: ')

    print('\nMétricas disponíveis para pesquisa: ')
    for metric in table[category]:
        print(metric)
    metric_choice = input('\nInsira uma métrica: ')

    ticker = input('\nInsira um ticker: ')
    url = f'https://api.gurufocus.com/public/user/{GF_API_TOKEN}/stock/{ticker}/financials'

    try:
        # Set a random User-Agent header
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        gf_request = Request(url, headers=headers)

        # Add a delay between requests to avoid rate limits
        time.sleep(2)  # You can adjust the delay time as needed

        gf_info = urlopen(gf_request).read()
        data = json.loads(gf_info.decode('utf8'))
        print(f'{metric_choice}:')
        # print(data)
        for info in data['financials']['annuals'][category][metric_choice]:
            print(info)

    except Exception as e:
        print(e)


def get_financial_info(ticker, category, metric):
    """
    Function returns a GuruFocus company financial satement metric using GF's API.
    Used in finedu_portfolio/views.py
    """
    url = f'https://api.gurufocus.com/public/user/{GF_API_TOKEN}/stock/{ticker}/financials'
    # url_2 = f'https://api.gurufocus.com/public/user/{GF_API_TOKEN}/stock/{ticker}/summary'

    # Set a random User-Agent header
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    gf_request = Request(url, headers=headers)
    # gf_request_2 = Request(url_2, headers=headers)

    # Add a delay between requests to avoid rate limits
    time.sleep(2)  # You can adjust the delay time as needed

    gf_info = urlopen(gf_request).read()
    data = json.loads(gf_info.decode('utf8'))

    # gf_info_2 = urlopen(gf_request_2).read()
    # financial_info_summary = json.loads(gf_info_2.decode('utf8'))

    # currency_info = financial_info_summary['summary']['general']['currency']
    # sector = financial_info_summary['summary']['general']['sector']

    financial_info_timeline = data['financials']['annuals']['Fiscal Year']
    financial_info = data['financials']['annuals'][category][metric]
    return financial_info_timeline, financial_info


# get_gf_summary()

# get_gf_metric()
