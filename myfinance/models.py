from django.db import models
from authuser.models import FCUser
import datetime
import django
def get_stats_csv_path(self,filename):
    return f'csv/{self.userfc.username}/stats/{self.userfc.pk}/{"stats.csv"}'
def get_current_stats_path(self):
    return f'csv/{self.userfc.username}/current_stats/{self.userfc.pk}/{"monthlystats.csv"}'
# Create your models here.
class Analytics(models.Model):
    userfc=models.ForeignKey(FCUser,on_delete=models.CASCADE)
    
    stats=models.FileField(max_length=255, upload_to=get_stats_csv_path,null=True,blank=True)
    currentstats=models.FileField(max_length=255, upload_to=get_current_stats_path,null=True,blank=True)
    last_updated=models.DateField(max_length=25,default=django.utils.timezone.now,blank=True,null=True)
    expenses=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    savings=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    saving_goal=models.DecimalField(max_digits=8,decimal_places=2,default=0)





