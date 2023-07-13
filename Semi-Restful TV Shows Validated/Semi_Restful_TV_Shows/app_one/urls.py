from django.urls import path
from . import views

urlpatterns = [
    path ('', views.default),
    path('shows' ,views.index ),
    path('shows/new', views.new),
    path('shows/create', views.create),
    path('shows/<int:id>', views.show) ,
    path ('shows/<int:id>/edit' , views.show_edit) ,
    path ('shows/edit' , views.edit) ,
    path ('shows/<int:num>/destroy' , views.destroy)
]
