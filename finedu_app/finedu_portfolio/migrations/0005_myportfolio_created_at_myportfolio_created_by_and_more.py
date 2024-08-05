# Generated by Django 5.0.6 on 2024-06-19 11:05

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finedu_portfolio', '0004_myportfolio'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='myportfolio',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myportfolio',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_portfolio_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='myportfolio',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='myportfolio',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_portfolio_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CompanyHolding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_shares', models.PositiveIntegerField()),
                ('price_paid_per_share', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(choices=[('USD', '$'), ('EUR', '€'), ('GBP', '£'), ('CAD', '$C'), ('AUD', '$AU'), ('SEK', 'kr'), ('JPY', '¥'), ('ILS', '₪')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finedu_portfolio.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holding_created_by', to=settings.AUTH_USER_MODEL)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finedu_portfolio.myportfolio')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holding_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Company Holding',
                'verbose_name_plural': 'Company Holdings',
            },
        ),
    ]
