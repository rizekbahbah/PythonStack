from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_login_regi),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('add/car', views.add_car),
    path('edit/<int:id>', views.render_edit_car),
    path('edit/car', views.edit_car),
    path('delete/<int:id>', views.delete_car,name="del_car"),
    path('cars', views.cars_show),
    path('show/<int:id>', views.car_show,name="show_car"),
]