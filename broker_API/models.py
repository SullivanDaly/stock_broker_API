from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()

    class Meta:
        abstract = True


class Investor(UserProfile):
    # Fields specific to Investor
    pass


class Admin(UserProfile):
    # Fields specific to Admin
    pass


class Stock(models.Model):
    name = models.CharField(max_length=255)
    ticker_symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Portfolio(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('investor', 'stock')