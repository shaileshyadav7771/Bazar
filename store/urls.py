from django.urls import path
from . import views

urlpatterns = [
    #here we are keeping '' blank becz after store/ nothing is there.
    path('',views.store , name='store'),
    path('<slug:category_slug>/', views.store, name='product_by_category'),

]