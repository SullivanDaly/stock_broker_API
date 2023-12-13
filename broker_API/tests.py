from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Stock, Investor, Admin, Investor, Portfolio
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

class StockModelTest(TestCase):

    def test_stock_creation(self):
        stock = Stock.objects.create(name="Test Stock", ticker_symbol="TS", price=100.50)
        self.assertEqual(stock.name, "Test Stock")
        self.assertEqual(stock.ticker_symbol, "TS")
        self.assertEqual(stock.price, 100.50)

class InvestorModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="john", email="john@example.com", password="secret")
        self.investor = Investor.objects.create(user=self.user, date_of_birth="1990-01-01", address="123 Main St")

    def test_investor_fields(self):
        """ Test the fields of the investor model """
        self.assertEqual(self.investor.user.username, "john")
        self.assertEqual(self.investor.user.email, "john@example.com")
        self.assertEqual(self.investor.date_of_birth, "1990-01-01")
        self.assertEqual(self.investor.address, "123 Main St")

    def test_investor_update(self):
        """ Test updating the investor"s details """
        self.investor.address = "456 Elm St"
        self.investor.save()
        self.assertEqual(self.investor.address, "456 Elm St")

class AdminModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="john", email="john@example.com", password="secret")
        self.admin = Admin.objects.create(user=self.user, date_of_birth="1990-01-01", address="123 Main St")

    def test_admin_fields(self):
        """ Test the fields of the admin model """
        self.assertEqual(self.admin.user.username, "john")
        self.assertEqual(self.admin.user.email, "john@example.com")
        self.assertEqual(self.admin.date_of_birth, "1990-01-01")
        self.assertEqual(self.admin.address, "123 Main St")

    def test_admin_update(self):
        """ Test updating the admin"s details """
        self.admin.address = "456 Elm St"
        self.admin.save()
        self.assertEqual(self.admin.address, "456 Elm St")

class StockModelTest(TestCase):

    def setUp(self):
        Stock.objects.create(name="Test Stock", ticker_symbol="TST", price=Decimal("123.45"))

    def test_stock_creation(self):
        """Test the creation of a stock and its fields."""
        stock = Stock.objects.get(ticker_symbol="TST")
        self.assertEqual(stock.name, stock.name)
        self.assertEqual(stock.name, "Test Stock")
        self.assertEqual(stock.price, Decimal("123.45"))

    def test_stock_price(self):
        """Test the stock price field."""
        stock = Stock.objects.get(ticker_symbol="TST")
        self.assertTrue(isinstance(stock.price, Decimal))



class PortfolioModelTest(TestCase):

    def setUp(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_investor = Investor.objects.create(user=test_user, date_of_birth="1990-01-01", address="123 Main St")
        test_stock = Stock.objects.create(name="Test Stock", ticker_symbol="TST", price=100.00)
        Portfolio.objects.create(investor=test_investor, stock=test_stock, quantity=10)

    def test_portfolio_content(self):
        portfolio = Portfolio.objects.get(id=1)
        expected_investor = portfolio.investor.user.username
        expected_stock_name = portfolio.stock.name
        expected_quantity = portfolio.quantity
        self.assertEqual(expected_investor, "testuser")
        self.assertEqual(expected_stock_name, "Test Stock")
        self.assertEqual(expected_quantity, 10)

class ViewTestCase(TestCase):
    def setUp(self):
        self.user_investor = User.objects.create_user(username="investor", password="password")
        self.user_admin = User.objects.create_user(username="admin", password="password")
        self.investor = Investor.objects.create(user=self.user_investor, date_of_birth="1990-01-01", address="123 Main St")
        self.admin = Admin.objects.create(user=self.user_admin, date_of_birth="1990-01-01", address="123 Main St")
        self.stock = Stock.objects.create(name="Test Stock", ticker_symbol="TST", price=Decimal("123.45"))
        self.client = APIClient()

    def get_investor_token(self):
        access = AccessToken.for_user(self.user_investor)
        return str(access)

    def get_admin_token(self):
        access = AccessToken.for_user(self.user_admin)
        return str(access)
    
    def test_investor_authentication(self):
        response = self.client.post("/broker_API/token/", {"username": "investor", "password": "password"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_admin_authentication(self):
        response = self.client.post("/broker_API/token/", {"username": "admin", "password": "password"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_buy_stocks(self):
        Portfolio.objects.create(investor=self.investor, stock=self.stock, quantity=10)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_investor_token())
        response = self.client.post("/broker_API/stocks/buy/", {"stock_name": self.stock.name, "quantity": 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Portfolio.objects.get(investor=self.investor, stock=self.stock).quantity, 20)

    def test_sell_stocks(self):
        Portfolio.objects.create(investor=self.investor, stock=self.stock, quantity=10)
        
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_investor_token())
        response = self.client.post("/broker_API/stocks/sell/", {"stock_name": self.stock.name, "quantity": 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Portfolio.objects.get(investor=self.investor, stock=self.stock).quantity, 5)

    def test_create_stock_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_admin_token())
        response = self.client.post("/broker_API/stocks/create/", {"name": "New Stock", "ticker_symbol": "NS", "price": "111.11"})
        self.assertEqual(response.status_code, 201)

    def test_edit_stock_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_admin_token())
        response = self.client.put("/broker_API/stocks/edit/" + self.stock.ticker_symbol + "/", {"name": "Edited Stock", "ticker_symbol": "ES", "price": "222.22"})
        self.assertEqual(response.status_code, 200)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.name, "Edited Stock")

    def test_delete_stock_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.get_admin_token())
        response = self.client.delete("/broker_API/stocks/delete/" + self.stock.ticker_symbol + "/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Stock.objects.count(), 0)

