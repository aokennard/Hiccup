import uuid

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django import forms



class NewHackathon(models.Model):
    title = models.CharField(max_length=50)
    sponsors = models.TextField(null=True)
    schedule = models.TextField(null=True)
    announcements = models.TextField(null=True)



class HackathonForm(ModelForm):
    class Meta:
        model = NewHackathon()
        fields = ['title', 'sponsors','schedule']
        print model.title

