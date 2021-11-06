from django.shortcuts import render
from .models import Product

# Create your views here.

def store(request):
	products=Product.objects.all().filter(is_available=True)
	product_counts=products.count()
	context = {
		'products' : products,
		'product_counts': product_counts,
	}


	return render(request,'store/store.html',context)