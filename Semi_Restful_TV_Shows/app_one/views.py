from django.shortcuts import render, redirect
from . import models


def default(request):
    return redirect('/shows')


def index(request):
    context = {
        "showAll": models.index()
    }

    return render(request, "show.html", context)


def new(request):
    return render(request, "create.html")


def create(request):
    models.creat(request)
    return redirect(f'/shows/{models.Show.objects.last().id}')


def show(request, id):
    context = {
        "show": models.show(id)
    }
    return render(request, 'show specific.html', context)


def show_edit(request, id):
    context = {
        "show": models.show(id)
    }
    return render(request, "edit.html", context)


def edit(request):
    x = request.POST['edit']
    models.edit(request, x)
    return redirect(f'/shows/{models.Show.objects.get(id=x).id}')


def destroy(request, num):
    models.destroy_show(num)
    return redirect('/shows')
