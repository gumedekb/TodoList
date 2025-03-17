from django.db import models
from django.contrib.auth.models import User


class TODOO(models.Model):
    srno=models.AutoField(primary_key=True, auto_created=True)  # Primart key
    title=models.CharField(max_length=100)  
    date=models.DateTimeField(auto_now_add=True)  
    status=models.BooleanField(default=False, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key for specific user 
