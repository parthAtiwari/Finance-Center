from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.userauth,name='userauth'),
    path('register/',views.register_user,name='register_user'),
    path('login/',views.login_user,name='login_user'),
    path('register/validate/',views.validate_details,name='validate_details'),
    path('login/authenticate/',views.login_auth,name='login_auth'),
    path('logout/',views.logout_user,name='logout_user'),
    path('editdetails/',views.editdetails,name='editdetails'),
    path('editdetails/validate/',views.editdetails_validate,name='editdetails_validate')

    
]