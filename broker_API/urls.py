from django.urls import path
from .views import StockListView, InvestorPortfoliosView, BuyStockView, SellStockView, StockCreateView, StockEditDeleteView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('stocks', StockListView.as_view(), name='list-stock'),
    path('stocks/list/', StockListView.as_view(), name='list-stock'),
    path('stocks/buy/', BuyStockView.as_view(), name='buy-stock'),
    path('stocks/sell/', SellStockView.as_view(), name='sell-stock'),
    path('stocks/create/', StockCreateView.as_view(), name='create-stock'),
    path('stocks/edit/<str:name_or_symbol>/', StockEditDeleteView.as_view(), name='edit-stock'),
    path('stocks/delete/<str:name_or_symbol>/', StockEditDeleteView.as_view(), name='delete-stock'),
    path('investor_portfolios/', InvestorPortfoliosView.as_view(), name='investor-portfolios'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
]