from rest_framework import serializers
from .models import Stock, Portfolio

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['name', 'ticker_symbol', 'price']

class PortfolioSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = ['stock', 'quantity']

class TransactionSerializer(serializers.Serializer):
    stock_name = serializers.CharField(max_length=256)
    quantity = serializers.IntegerField()