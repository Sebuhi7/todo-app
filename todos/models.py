from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from django.db.models.fields import TextField

class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    user_to = models.ForeignKey(User,related_name='user',on_delete=models.PROTECT,blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField('Description', blank=True, null=True)
    due_to = models.DateTimeField('Due To', blank=True, null=True)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    update_at = models.DateTimeField('Updated', auto_now=True)
    send_to = models.BooleanField(default=False,null=True,blank=True)
    send_from = models.BooleanField(default=False,null=True,blank=True)
    read_only = models.BooleanField(default=False,null=True,blank=True)
    isCompleted = models.BooleanField(default=False,null=True,blank=True)
    comment = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title