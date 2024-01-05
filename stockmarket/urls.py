from django.contrib import admin
from django.urls import path,include
from . import views
from .views import StockMarket
urlpatterns = [
    path('',StockMarket.marketwatch,name='marketwatch'),
    path('gainers',StockMarket.day_gainers,name='day_gainers'),
    path('losers',StockMarket.day_losers,name='day_losers'),
    path('mostactive',StockMarket.most_active,name='most_active')
]