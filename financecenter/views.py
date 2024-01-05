from django.shortcuts import render,redirect
from authuser.models import FCUser
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
import requests
import json
# url = "https://bing-news-search1.p.rapidapi.com/news/search"

# querystring = {"q":"Business,Finance,Stock Market","cc":"IN","count":"5","freshness":"Day","textFormat":"Raw","safeSearch":"Off"}

# headers = {
#     "X-BingApis-SDK": "true",
#     "X-RapidAPI-Key": "fd556575ecmshf2d72d702e6e497p19bc0bjsn9c7c37adf16a",
#     "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
# }
# return render(request,'dashboard.html')


def fchome(request):
    return render(request,'financecenter.html')
def display_profile(request):
    if request.user.is_authenticated:

        obj=FCUser.objects.all().filter(username=request.user)
        userobj=FCUser.objects.get(username=request.user)
        pic=userobj.profile_picture
        profile=obj.values()[0]
        name=profile['first_name']+' '+profile['last_name']
        username=profile['username']
        user_pic=f'/media/{pic}'
        items=('password','is_staff','is_superuser','id','user_ptr_id','last_login','is_active','profile_picture')
        for i in items:
            del profile[i]
        birthday=profile['date_of_birth']==datetime.date.today()


        return render(request,'userprofile.html',{'profile':profile.items(),'name':name,'username':username,'birthday':birthday,'user_pic':user_pic})
    else:
        messages.add_message(request,messages.ERROR,'Login to view profile')
        return redirect('/')
    
@login_required()
def user_dashboard(request):
    
    
    
    response=requests.request(url="https://api.nytimes.com/svc/topstories/v2/business.json?api-key=okTUDhrhmLwJ3uCzvlMhGQDz1UsuBpXY",method='GET')
    
    news=json.loads(response.text)

   
    

        
    
    
    news=list(news['results'])
    

    return render(request,'dashboard.html',{'news':news})
    
def aboutus(request):
    return render(request,'aboutus.html')
def developer_contact(request):
    return render(request,'dev-contact.html')

# async def marketwatch(request):
    

#     url = "https://trading-view.p.rapidapi.com/market/get-movers"

    

#     headers = {
#         "X-RapidAPI-Key": "fd556575ecmshf2d72d702e6e497p19bc0bjsn9c7c37adf16a",
#         "X-RapidAPI-Host": "trading-view.p.rapidapi.com"
#     }
#     querystring = {"exchange":"NSE","name":"percent_change_gainers","locale":"en"}
#     async with aiohttp.ClientSession() as s:
#         gainers_response=asyncio.create_task(s.get(url,headers=headers,params=querystring))
#         # querystring = {"exchange":"NSE","name":"percent_change_loosers","locale":"en"}
#         # loosers_response=asyncio.create_task(s.get(url,headers=headers,params=querystring))
#         # querystring = {"exchange":"NSE","name":"volume_gainers","locale":"en"}
#         # volume_gainers_response=asyncio.create_task(s.get(url,headers=headers,params=querystring))
#         gainers=await gainers_response
#         print(gainers)
#         # day_gainers=json.loads(gainers.read())
#         # gainers=[]
#         # for i in day_gainers['symbols']:
#         #     d=dict()
#         #     d['symbol']=i['s']
#         #     d['change']=round(i['f'][0],2)
#         #     d['volume']=i['f'][1]
#         #     gainers.append(d)
#         # loosers=await loosers_response
#         # day_loosers=json.loads(loosers_response.text)
#         # loosers=[]
#         # for i in day_loosers['symbols']:
#         #     d=dict()
#         #     d['symbol']=i['s']
#         #     d['change']=round(i['f'][0],2)
#         #     d['volume']=i['f'][1]
#         #     loosers.append(d)

#         # volumegainers=await volume_gainers
#         # volume_gainers=json.loads(volume_gainers_response.text)
#         # volumegainers=[]
#         # for i in volume_gainers['symbols']:
#         #     d=dict()
#         #     d['symbol']=i['s']
#         #     d['volume']=i['f'][1]
#         #     volumegainers.append(d)
#         return render(request,'marketwatch.html')

        
        