from django.db import models
from django.shortcuts import render, redirect

class ShowManager(models.Manager):
    def basic_validator(self , postData):
        errors= {}

        if len(postData['title']) < 2 :
            errors['title'] = "Show Title should be at least 2 characters"
        if len(postData['network']) < 3 :
            errors['network'] = "Show Network-name should be at least 3 characters"
        if len(postData['description']) < 10:
            errors['description'] = "Show description should be at least 10 characters"
        return errors

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=45)
    release_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()


def index ():
    return Show.objects.all()

def creat(request):
    Show.objects.create(title=request.POST['title'],
                        network=request.POST['network'],
                        release_date=request.POST['date'],
                        description=request.POST['description'])

def show(id):
    return Show.objects.get(id=id)

def edit(request,x):
    update_Show = Show.objects.get(id=x)
    update_Show.title = request.POST['title'] 
    update_Show.network = request.POST['network'] 
    update_Show.release_date = request.POST['date'] 
    update_Show.description = request.POST['description'] 
    update_Show.save()

def destroy_show (num):
    Show_to_delete=Show.objects.get(id=num)
    Show_to_delete.delete()
