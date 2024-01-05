from django.shortcuts import render, redirect
from .models import FCUser
from .serializers import FCUserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myfinance.views import *
import datetime
from myfinance.models import Analytics

# Create your views here.


def userauth(request):

    return render(request, 'financecenter.html')


def login_user(request):
    if request.user.is_authenticated:
        messages.add_message(request,messages.ERROR,'Already logged in')
        return redirect('/')
    else:

        return render(request, 'login.html')


def register_user(request):
    if request.user.is_anonymous:

        return render(request,'register.html')
    else:
        messages.add_message(request,messages.ERROR,'Logout First')
        return redirect(to='/')

# @api_view(http_method_names=['GET'])
# @login_required()
def logout_user(request):
    
    if not request.user.is_authenticated:
        messages.add_message(request,messages.ERROR,'Log in first')
        return redirect(to='/auth/login')

    try:

        logout(request)
        messages.add_message(request,messages.SUCCESS,'User logged out')
        return redirect(to='/auth/login')
        

    except Exception as e:
        return render(request,'financecenter.html',{'error':'Logout failed'})
        

def login_auth(request):
    if request.user.is_authenticated:
        messages.add_message(request,messages.ERROR,'Already logged in')
        return redirect(to='/')
    

    try:
        
        user_obj = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user_obj is not None:

            login(request, user_obj)
            
            messages.add_message(request,messages.SUCCESS,'Log in Successfull')
            
            if (instance:=Analytics.objects.get(userfc=request.user)).last_updated.month<datetime.date.today().month or instance.last_updated.year<datetime.date.today().year:
                 
               
                

                return redirect('/my-finance/reset-stats/')
                
            return redirect('/dashboard')

        else:
            messages.add_message(request,messages.ERROR,'Invalid Credentials')
            return redirect('/auth/login')

    except Exception as e:
        messages.add_message(request,messages.ERROR,'Invalid Credentials')
        return redirect('/auth/login')


def validate_details(request):

    
    if request.user.is_anonymous:


        try:

            if request.POST['password'] == request.POST['confirmpassword']:
                obj=FCUserSerializer(data=request.POST)
                obj.is_valid(raise_exception=True)
                
                obj = FCUser.objects.create_user(username=request.POST['username'], gender=request.POST['gender'],first_name=request.POST['first_name'],last_name=request.POST['last_name'], email=request.POST['email'], date_of_birth=request.POST['date_of_birth'])
                if request.FILES:
                    obj.profile_picture=request.FILES['profile_pic']
                obj.set_password(request.POST['password'])
                obj.save()
                create_monthly_csv(obj)
                create_stats_csv(obj)
                create_financial_model(obj)
                messages.add_message(request,messages.SUCCESS,'User Registered')
                return redirect('/auth/login')

            else:
                messages.add_message(request,messages.ERROR,'Password do not match')
                return redirect('/auth/register')

        except Exception as e:
            messages.add_message(request,messages.ERROR,e.__str__())
            return redirect('/auth/register')
    
        
    else:
        messages.add_message(request,messages.ERROR,'logout first')
        return redirect('/')
    
@login_required()
def editdetails(request):
    return render(request,'register.html')

@login_required()
def editdetails_validate(request):
    try:
           
        # if request.POST['password']==request.POST['confirmpassword']:

        #     obj=FCUser.objects.get(username=request.user.username)
            
        #     new_obj=FCUserSerializer(data=request.POST)
        #     new_obj.is_valid(raise_exception=True)
            
        #     obj.username=request.POST['username']
        #     obj.first_name=request.POST['first_name']
        #     obj.last_name=request.POST['last_name']
        #     obj.email=request.POST['email']
        #     obj.gender=request.POST['gender']
        #     obj.date_of_birth=request.POST['date_of_birth']
            
        #     obj.save()
            
        #     messages.add_message(request,messages.SUCCESS,'Details Saved')

            return redirect('/profile')
        # else:
        #     messages.add_message(request,messages.ERROR,'Confirmed password do not match')
        #     return render('/profile')
    except Exception as e:
        messages.add_message(request,messages.ERROR,e.__str__)
        return redirect('/profile')
    
