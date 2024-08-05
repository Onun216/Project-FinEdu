from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_summernote.models import AbstractAttachment
from utils.images import resize_image
from utils.rands import slugify_new

# class UserPortfolio(models.Model):


class Company(models.Model):

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10)
    # in_portfolio = models.BooleanField(default=False)
    content = models.TextField()

    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    is_published = models.BooleanField(
        default=False,
        help_text=(''),)

    cover = models.ImageField(
        upload_to='company_pics/%Y/%m/', blank=True, default='')
    cover_in_content = models.BooleanField(
        default=True,
        help_text='',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='company_created_by'
    )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='company_updated_by'
    )

    def __str__(self) -> str:
        return f'{self.name} - {self.ticker}'

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:post', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.ticker, 4)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save


class MyPortfolio(models.Model):
    class Meta:
        verbose_name = 'My Portfolio'
        verbose_name_plural = 'My Portfolios'

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='my_portfolio_created_by'
    )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='my_portfolio_updated_by'
    )

    def __str__(self) -> str:
        return f'{self.name}'


class CompanyHoldingManager(models.Manager):
    def group_by_company(self):
        """
        Groups CompanyHolding objects by company name.

        Returns:
          A dictionary where keys are company names and values are lists of 
          CompanyHolding objects for that company.
        """
        holdings = self.all()
        grouped_holdings = {}
        for holding in holdings:
            company_name = holding.company.name
            if company_name not in grouped_holdings:
                grouped_holdings[company_name] = []
            grouped_holdings[company_name].append(holding)

        return dict(sorted(grouped_holdings.items()))

    def sum_shares(self):
        """
        Calls group_by_company: It reuses the existing functionality to group holdings by company name.
        Initializes a dictionary total_shares: This dictionary will store the company name as the key and the total number of shares held for that company as the value.
        Iterates through grouped holdings: It loops through each company and its corresponding holdings list obtained from group_by_company.
        Accumulates shares for each company: For each holding within a company's holdings list, it adds the number_of_shares to the corresponding company's total in the total_shares dictionary.
        Returns the total_shares dictionary: This dictionary contains the desired results, where each key-value pair represents a company and the total number of shares held for that company.
        """
        holdings = self.group_by_company()
        total_shares = {holding: 0 for holding in holdings.keys()}
        for company, holdings in holdings.items():
            for holding in holdings:
                total_shares[company] += holding.number_of_shares
        return total_shares

    def holding_cost(self):
        # holdings = self.group_by_company()
        return None


class CompanyHolding(models.Model):
    objects = CompanyHoldingManager()

    class Meta:
        verbose_name = 'Company Holding'
        verbose_name_plural = 'Company Holdings'

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(MyPortfolio, on_delete=models.CASCADE)
    number_of_shares = models.PositiveIntegerField()
    price_paid_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(null=False)
    currency = models.CharField(choices=(
        ('$', 'USD'),
        ('€', 'EUR'),
        ('£', 'GBP'),
        ('$C', 'CAD'),
        ('$AU', 'AUD'),
        ('kr', 'SEK'),
        ('¥', 'JPY'),
        ('₪', 'ILS')
    ))

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='holding_created_by'
    )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='holding_updated_by'
    )

    def __str__(self):
        return f"{self.company.name} - {self.number_of_shares} shares @ {self.currency}{self.price_paid_per_share} on {self.purchase_date}"


class FinancialStatementCategory(models.Model):
    class Meta:
        verbose_name = 'Financial Statement Category'
        verbose_name_plural = 'Financial Statement Categories'

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # user.post_set.all() -> query que vai buscar todos os posts do utilizador
    # Gera um erro porque a relação não é especificada, gerando um conflito.
    # Correcção: user.post_created_by.all()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='fs_category_created_by'
    )

    def __str__(self) -> str:
        return self.name


class FinancialStatementMetric(models.Model):
    class Meta:
        verbose_name = 'Financial Statement Metric'
        verbose_name_plural = 'Financial Statement Metrics'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(FinancialStatementCategory,
                                 on_delete=models.CASCADE,
                                 default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    # user.post_set.all() -> query que vai buscar todos os posts do utilizador
    # Gera um erro porque a relação não é especificada, gerando um conflito.
    # Correcção: user.post_created_by.all()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='fs_metric_created_by'
    )

    def __str__(self) -> str:
        return self.name
