from django.shortcuts import render, redirect
from . import models
from django.contrib import messages


def render_login_regi(request):
    return render(request, 'login_regi.html')


def register(request):
    errors = models.validate_regi(request)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        models.register(request)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        if models.login(request):
            return redirect('/dashboard')
    return redirect('/')


def logout(request):
    try:
        del request.session['user_id']
        redirect('/')
    except:
        pass
    return redirect('/')


def dashboard(request):
    id = request.session['user_id']
    user = models.get_user_by_id(id)
    cars = models.get_cars_all()
    context = {
        'user': user,
        'cars': cars,
    }
    return render(request, 'dashboard.html', context)


def add_car(request):
    user_id = request.session['user_id']
    user = models.get_user_by_id(user_id)
    errors = models.validate_presence(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        models.add_car(request, user)
    return redirect('/dashboard')


def render_edit_car(request, id):
    car = models.get_car_by_id(id)
    context = {
        'car': car,
    }
    return render(request, 'edit_car.html', context)


def edit_car(request):
    models.update_car(request)
    return redirect('/dashboard')


def delete_car(request, id):
    models.delete_car(id)
    return redirect('/dashboard')


def cars_show(request):
    cars = models.get_cars_all()
    context = {
        'car': cars,
    }
    return render(request, 'show_cars.html', context)


def car_show(request, id):
    car = models.get_car_by_id(id)
    context = {
        'car': car,
    }
    return render(request, 'show_car.html', context)



