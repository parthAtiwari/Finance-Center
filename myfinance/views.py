from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import os
import csv
from .models import Analytics
from authuser.models import FCUser
import datetime
from django.contrib import messages
# from PyPDF2 import *

# import PyPDF2
import requests
import pandas as pd

# Create your views here.
@login_required()
def my_finance(request):
    try:

        month_stats_file_path = f'media/csv/{request.user.username}/current_stats/{request.user.pk}/monthlystats.csv'
        
        # current data
        cr_data=pd.read_csv(month_stats_file_path)
        expenses=cr_data[cr_data['CashFlowType']=='E']
        savings=cr_data[cr_data['CashFlowType']=='S']
        expenses=expenses.to_dict()
        savings=savings.to_dict()
        expenses['Amount']=list(expenses['Amount'].values())
        savings['Amount']=list(savings['Amount'].values())
        expenses['Name']=list(expenses['Name'].values())
        savings['Name']=list(savings['Name'].values())
        expenses['Description']=list(expenses['Description'].values())
        savings['Description']=list(savings['Description'].values())
    
        obj=Analytics.objects.get(userfc=request.user)
    
        goal=obj.saving_goal
        mysavings=obj.savings
        myexpenses=obj.expenses
        #prev_stats
        stats_file_path = f'media/csv/{request.user.username}/stats/{request.user.pk}/stats.csv'
        stats_data=pd.read_csv(stats_file_path)
        stats_data=stats_data.tail(12)
        stats_data=stats_data.to_dict()
    
        stats_data['Expenses']=list(stats_data['Expenses'].values())
        stats_data['Savings']=list(stats_data['Savings'].values())
        stats_data['Labels']=list(stats_data['MM-YYYY'].values())
        
        expense_count=sum([0 if e<=s else 1 for e,s in zip(stats_data['Expenses'],stats_data['Savings'])])

    

        return render(request,'finance.html',{'expenses':expenses,'savings':savings,'goal':goal,'stats':stats_data,'mysavings':mysavings,'myexpenses':myexpenses,'count':expense_count})
    except Exception as e:
        return redirect('create-fin-model/')
@login_required()
def userinput(request):
    return render(request,'userinput.html')

# @login_required()
def write_to_csv(path,file,towhich,*args,**kwargs):
    with open(path+file, 'w', newline='') as csvfile:
        writefile = csv.writer(csvfile)
        if towhich=='current-stats':

            writefile.writerow(['Name','Amount','Description','CashFlowType'])
            
        elif towhich=='stats':
            writefile.writerow(['Expenses','Savings','MM-YYYY'])
            

        # csvfile.close()
    return 


def create_stats_csv(csv_user):
    file_path = f'media/csv/{csv_user.username}/stats/{csv_user.pk}'
    os.makedirs(file_path,mode=0o777,exist_ok=True)
    write_to_csv(file_path,'/stats.csv','stats')

    

def create_monthly_csv(csv_user):
    
    file_path = f'media/csv/{csv_user.username}/current_stats/{csv_user.pk}'
    os.makedirs(file_path,mode=0o777,exist_ok=True)
    write_to_csv(file_path,'/monthlystats.csv','current-stats')
    

def create_financial_model(fin_user):


    fin_obj=Analytics(userfc=fin_user)
    fin_obj.save()
    

@login_required()
def reset_monthly_stats(request):
    obj=FCUser.objects.get(username=request.user.username)
    file_path = f'media/csv/{obj.username}/current_stats/{obj.pk}'
    write_to_csv(file_path,'/monthlystats.csv','current-stats')
    
    
    
    with open(f'media/csv/{obj.username}/stats/{obj.pk}/stats.csv', 'a', newline='') as stats_csvfile:
            writefile = csv.writer(stats_csvfile)
            writefile.writerow([0,0,str(datetime.date.today().month)+'-'+str(datetime.date.today().year)])
            # stats_csvfile.close()
    #updating stats
    stats_instance=Analytics.objects.get(userfc=request.user)
    stats_instance.last_updated=datetime.date.today()
    stats_instance.expenses=0
    stats_instance.savings=0
    stats_instance.saving_goal=0
    stats_instance.save()
    return redirect('/dashboard')


def clear_stats_line(filename):
    with open(filename, 'rb+') as file:
        file.seek(-2, os.SEEK_END) 
        while  file.read(1)!= b'\n': 
      
            file.seek(-2, os.SEEK_CUR)
  
        file.truncate()
    return


@login_required()
def saveinfo(request):
    month_stats_file_path = f'media/csv/{request.user.username}/current_stats/{request.user.pk}/monthlystats.csv'
    stats_file_path=f'media/csv/{request.user.username}/stats/{request.user.pk}/stats.csv'
    data=list(zip(request.POST.getlist('name'),request.POST.getlist('amount'),request.POST.getlist('desc'),request.POST.getlist('cashflowtype')))
    
    with open(month_stats_file_path, 'a', newline='') as monthly_csvfile:
        writefile = csv.writer(monthly_csvfile)
        writefile.writerows(data)
        
      
        # monthly_csvfile.close()
    # stats_obj=Analytics.objects.get(userfc=request.user)
    expenses,savings=0,0
    for d in data:
        if d[3]=='E':
            expenses+=int(d[1])
        elif d[3]=='S':
            savings+=int(d[1])
    
    stats_obj=Analytics.objects.get(userfc=request.user)
    stats_obj.expenses=stats_obj.expenses+expenses
    stats_obj.savings=stats_obj.savings+savings
    stats_obj.last_updated=datetime.date.today()
    stats_obj.save()
    with open(stats_file_path, 'r') as statsfile:
        lines = statsfile.readlines()
        
        if len(lines)>1:

            clear_stats_line(stats_file_path)
        
    with open (stats_file_path,'a',newline='') as stats_file:
        writefile=csv.writer(stats_file)
        writefile.writerow([stats_obj.expenses,stats_obj.savings,str(stats_obj.last_updated.month)+'-'+str(stats_obj.last_updated.year)])



    return redirect('/my-finance')
@login_required
def save_goal(request):
    obj=Analytics.objects.get(userfc=request.user)
    if (goal:=int(request.POST['saving-goal']))>obj.saving_goal:
        messages.add_message(request,messages.SUCCESS,'Saving Target Saved.')
        obj.saving_goal=goal
        obj.save()
    else:
         messages.add_message(request,messages.ERROR,'Target amount can\'t be decreased')

    return redirect('/my-finance')



        # Create a CSV reader object
        # csvreader = csv.reader(stats_csvfile)
            
        # # Move the file pointer to the end of the file
        # stats_csvfile.seek(0, 2)
        # stats_csvfile.seek(0, 2)
        # pos = stats_csvfile.tell()
        # print(pos)
        # # Read the file backwards line by line until you find the last non-empty line
        # while pos > 0:
        #     pos -= 1
        #     stats_csvfile.seek(pos, 0)
        #     if stats_csvfile.read(1) == '\n':
        #         last_line = stats_csvfile.readline().strip()
        #         if last_line:
        #             break

        # # Parse the last line as a CSV row to get the data
        # print(stats_csvfile.tell())

        # last_row = list(csv.reader([last_line]))[0]
        # print(stats_csvfile.tell())
        # print(last_row)
        # stats_csvfile.close()


    # if not flag:
    #     with open(stats_file_path, 'a', newline='') as stats_csvfile:
    #         writefile = csv.writer(stats_csvfile)
    #         writefile.writerow([expenses,savings,datetime.date.today()])
            
    #         monthly_csvfile.close()


    
    
  

def init_fin_model(request):
    user_obj=FCUser.objects.get(username=request.user)
    create_financial_model(user_obj)
    messages.add_message(request,messages.SUCCESS,'Created User Analytics Model')
    return redirect('/my-finance')

# def reset_files(request):
#     for i in FCUser.objects.all():
#         create_monthly_csv(i)
#         create_stats_csv(i)
#     messages.add_message(request,messages.SUCCESS,'files reset')
#     return redirect('/')

# def reset_analytics(request):
#     for i in Analytics.objects.all():
#         i.last_updated=datetime.datetime(2023,5,17)
#         i.save()
#     messages.add_message(request,messages.SUCCESS,'analytics reset')
#     return redirect('/')