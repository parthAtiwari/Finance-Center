from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
import json
import copy

# Create your views here.

class StockMarket:
    
    URL="https://trading-view.p.rapidapi.com/market/get-movers"
    querystring = {"exchange":"NSE","locale":"en"}
    HEADERS= {
    'X-RapidAPI-Key': 'Your Key',
    'X-RapidAPI-Host': 'trading-view.p.rapidapi.com'
  }
    
    @login_required
    
    def marketwatch(request):
        url = "https://trading-view.p.rapidapi.com/stocks/get-financials"
        symbols=['TITAN','TATAMOTORS']
        watchlist={'data':[]}
        for symbol in symbols:

            querystring = {"columns":"name,change,open,close,average_volume,volume,price_52_week_high,price_52_week_low","symbol":'NSE:'+symbol,"screenerName":"india","lang":"en"}

            response = requests.request("GET", url, headers=StockMarket.HEADERS, params=querystring)
            data=json.loads(response.text)
            # print(data)
            
            watchlist['data'].append(data['data'][0]['d'])
        
        
        watchlist['columns']=list(querystring['columns'].split(','))
 
        return render(request,'marketwatch.html',{'watchlist':watchlist})


    @login_required()
    
    def day_gainers(request):
        querystring=copy.deepcopy(StockMarket.querystring)
        querystring['name']='percent_change_gainers'
        response = requests.request("GET",StockMarket.URL, headers=StockMarket.HEADERS, params=querystring)
        
        day_gainers=json.loads(response.text)
        gainers=[]
     
        for i in day_gainers['symbols']:
            d=dict()
            d['symbol']=i['s']
            d['change']=round(i['f'][0],2)
            d['volume']=i['f'][1]
            gainers.append(d)
        
        return render(request,'marketwatch.html',{'gainers':gainers})
    

    @login_required()
    # @classmethod
    def day_losers(request):

        querystring=copy.deepcopy(StockMarket.querystring)
        querystring['name']='percent_change_loosers'
        response = requests.request("GET",StockMarket.URL, headers=StockMarket.HEADERS, params=querystring)
        day_loosers=json.loads(response.text)
        losers=[]
        for i in day_loosers['symbols']:
            d=dict()
            d['symbol']=i['s']
            d['change']=round(i['f'][0],2)
            d['volume']=i['f'][1]
            losers.append(d)
        return render(request,'marketwatch.html',{'losers':losers})
    
    
    @login_required()
    # @classmethod
    def most_active(request):
        querystring=copy.deepcopy(StockMarket.querystring)
        querystring['name']='volume_gainers'
        response = requests.request("GET", StockMarket.URL, headers=StockMarket.HEADERS, params=querystring)
        volume_gainers=json.loads(response.text)
        volumegainers=[]
        for i in volume_gainers['symbols']:
            d=dict()
            d['symbol']=i['s']
            d['volume']=i['f'][1]
            volumegainers.append(d)
        return render(request,'marketwatch.html',{'volume_gainers':volumegainers})
    
