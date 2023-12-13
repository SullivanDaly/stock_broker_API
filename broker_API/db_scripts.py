import random
import threading
import time
from faker import Faker
from decimal import Decimal
from broker_API.models import Investor, Admin, Stock, Portfolio
from django.contrib.auth.models import User

# Number of each record to create
num_investors = 10
num_admins = 5
num_stocks = 20

fake = Faker()

def create_user_profile(user_class, n):
    for _ in range(n):
        user = User.objects.create_user(username=fake.user_name(),
                                        email=fake.email(),
                                        password='password')
        profile = user_class.objects.create(user=user,
                                  date_of_birth=fake.date_of_birth(),
                                  address=fake.address())
        profile.save()

def create_stocks(n):
    for _ in range(n):
        stock = Stock.objects.create(name=fake.company(),
                             ticker_symbol=fake.lexify(text='????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                             #description=fake.text(),
                             price=Decimal(fake.random_number(digits=3)))
        stock.save()

def create_portfolios():
    investors = Investor.objects.all()
    stocks = Stock.objects.all()
    for investor in investors:        
        nb_stock = random.randint(1, 5)  # Each investor buys 1-5 stocks
        random_stocks = Stock.objects.order_by('?')[:nb_stock]
        for stock in random_stocks:
            portfolio = Portfolio.objects.create(investor=investor,
                                    stock=stock,
                                    quantity=random.randint(1, 100),
                                    # purchase_price=stock.price,
                                    # purchase_date=fake.date_between(start_date='-2y', end_date='today')
                                    )
            portfolio.save()

def populate():
    print('Populating database...')
    create_user_profile(Investor, num_investors)
    create_user_profile(Admin, num_admins)
    create_stocks(num_stocks)
    create_portfolios()



def update_stock_prices():
    while True:
        print('Updating stock prices...')
        stocks = Stock.objects.all()
        for stock in stocks:
            stock.price += Decimal(random.uniform(-10.0, 10.0))
            stock.save()
        time.sleep(10)

def start_update_stock_prices_thread():
    thread = threading.Thread(target=update_stock_prices)
    thread.daemon = True  # Daemonize thread
    thread.start()