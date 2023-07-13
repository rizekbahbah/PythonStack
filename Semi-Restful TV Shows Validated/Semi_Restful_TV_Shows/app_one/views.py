from django.shortcuts import render, redirect 
from . import models
from django.contrib import messages
from .models import Show

def default(request):
    return redirect('/shows')

def index(request):
    context={
    "showAll":models.index()
    }

    return render (request , "show.html" , context)

def new(request):
    return render(request, "create.html")

def create(request):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key , value in errors.items():
            messages.error(request , value)
        return redirect('/shows/new')
    else :
        models.creat(request)
        return redirect(f'/shows/{models.Show.objects.last().id}' )

def show(request, id):
    context = {
        "show": models.show(id)
    }
    return render(request, 'show specific.html', context)

def show_edit(request,id):
    context = {
        "show": models.show(id)
    }
    return render (request ,"edit.html",context )

def edit(request):
    x= request.POST['edit']
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key , value in errors.items():
            messages.error(request , value)
        return redirect(f'/shows/{models.Show.objects.get(id=x).id}/edit')
    else:
        models.edit( request ,x )
        return redirect(f'/shows/{models.Show.objects.get(id=x).id}')


def destroy(request, num):
    models.destroy_show(num)
    return redirect('/shows')
