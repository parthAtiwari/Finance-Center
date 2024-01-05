from rest_framework import serializers
from .models import FCUser
class FCUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=FCUser
        fields=['username','email','first_name','last_name','password','gender','date_of_birth',]
        extra_kwargs={'password':{'write_only':True}}
     
    
    
    
    
