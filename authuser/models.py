from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser

def get_profile_pic_path(self,filename):
    return f'user_pics/{self.username}/{self.pk}/{"user_pic.png"}'
def get_default_pic_path():
    return 'default_pics/user/user.png'

class FCUser(User):

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, null=False, blank=False)
    date_of_birth = models.DateField(null=False)
    profile_picture=models.ImageField(max_length=255,upload_to=get_profile_pic_path ,blank=True,null=True,default=get_default_pic_path)
    

    
    
    # first_name = models.CharField(max_length=101, null=False)
    # last_name = models.CharField(max_length=101, null=False)
    # email = models.EmailField(null=False,primary_key=True)
    # username = models.CharField(max_length=101)
    # password = models.CharField(max_length=255)
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)
    # last_login = models.DateTimeField(auto_now=True)
    # date_joined = models.DateTimeField(auto_now=True)
    # email = models.EmailField(null=False,primary_key=True)

    # USERNAME_FIELD='email'
    # REQUIRED_FIELDS=['username']

    # class Meta:

    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['username', 'email'], name='user_email_combination'
    #         )
    #     ]
