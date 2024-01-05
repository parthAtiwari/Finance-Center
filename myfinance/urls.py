from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.my_finance,name='myfinance'),
    path('userinput/',views.userinput,name='userinput'),
    path('userinput/saveinfo/',views.saveinfo,name='saveinfo'),
    path('reset-stats/',views.reset_monthly_stats,name='reset_monthly_stats'),
    path('save-goal/',views.save_goal,name='save-goal'),
    path('create-fin-model/',views.init_fin_model,name='init-fin-model')
 

    # path('reset-files/',views.reset_files,name='reset-files'),
    # path('reset-analytics/',views.reset_analytics,name='reset-analytics')
    
    
]