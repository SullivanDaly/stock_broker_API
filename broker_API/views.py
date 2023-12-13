from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Stock, Investor, Admin, Portfolio
from .serializers import StockSerializer, PortfolioSerializer, TransactionSerializer

def get_object(self, name_or_symbol):
        try:
            return Stock.objects.get(name=name_or_symbol)
        except Stock.DoesNotExist:
            return Stock.objects.get(ticker_symbol=name_or_symbol)

class StockListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    get_queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned stocks to a given name,
        by filtering against a `name` query parameter in the URL.
        """
        stocks = Stock.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            stocks = stocks.filter(name__icontains=name)
        return stocks

class BuyStockView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            stock_name = serializer.validated_data['stock_name']
            quantity = serializer.validated_data['quantity']

            stock = get_object_or_404(Stock, name=stock_name)
            investor = request.user.investor

            portfolio, created = Portfolio.objects.get_or_create(
                investor=investor, stock=stock,
                defaults={'quantity': 0, 'purchase_price': stock.price}
            )
            portfolio.quantity += quantity
            portfolio.save()

            return Response({"message": "Stocks purchased successfully"}, status=200)
        return Response(serializer.errors, status=400)

class SellStockView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            stock_name = serializer.validated_data['stock_name']
            quantity = serializer.validated_data['quantity']

            stock = get_object_or_404(Stock, name=stock_name)
            investor = request.user.investor
            portfolio = get_object_or_404(Portfolio, investor=investor, stock=stock)

            if quantity >= portfolio.quantity:
                portfolio.delete()
                # We could have sent a message saying that we had not enough stocks to sell
                # but we chose to delete the portfolio instead for this example
            else:
                portfolio.quantity -= quantity
                portfolio.save()

            return Response({"message": "Stocks sold successfully"}, status=200)
        return Response(serializer.errors, status=400)

class InvestorPortfoliosView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        investor = self.request.user.investor
        portfolios = Portfolio.objects.filter(investor=investor)
        return portfolios

class StockCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        _ = self.request.user.admin
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class StockEditDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, name_or_symbol):
        try:
            return Stock.objects.get(name=name_or_symbol)
        except Stock.DoesNotExist:
            return Stock.objects.get(ticker_symbol=name_or_symbol)

    def put(self, request, name_or_symbol, format=None):
        _ = self.request.user.admin
        stock = self.get_object(name_or_symbol)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, name_or_symbol, format=None):
        _ = self.request.user.admin
        stock = self.get_object(name_or_symbol)
        stock.delete()
        return Response(status=204)