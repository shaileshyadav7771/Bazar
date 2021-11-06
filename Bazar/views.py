from django.shortcuts import render
from store.models import Product

def home(request):
	products=Product.objects.all().filter(is_available=True)

	context = {
		'products' : products,
	}

	# print('request jo aa rhi hai vo:',request)
	return render(request,'home.html', context)