from django.urls import path
from . import views

urlpatterns = [
    #here we are keeping '' blank becz after store/ nothing is there.
    path('',views.store , name='store'),

]