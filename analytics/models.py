from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SalesAnalytics(models.Model):
    date = models.DateField(unique=True)
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed_orders = models.IntegerField(default=0)
    cancelled_orders = models.IntegerField(default=0)
    peak_hour = models.IntegerField(default=12, help_text="Hour of day with most orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.date}"

    class Meta:
        verbose_name_plural = "Sales Analytics"
        ordering = ['-date']

class DailyOrderStats(models.Model):
    date = models.DateField(unique=True)
    hour_00_06 = models.IntegerField(default=0, help_text="Orders from 12am-6am")
    hour_06_12 = models.IntegerField(default=0, help_text="Orders from 6am-12pm")
    hour_12_18 = models.IntegerField(default=0, help_text="Orders from 12pm-6pm")
    hour_18_24 = models.IntegerField(default=0, help_text="Orders from 6pm-12am")
    
    def __str__(self):
        return f"Hourly stats for {self.date}"

class TopProduct(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    total_quantity_sold = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.total_quantity_sold} sold"

    class Meta:
        ordering = ['-total_quantity_sold']