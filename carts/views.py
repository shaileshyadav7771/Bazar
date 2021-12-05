from django.shortcuts import render

# Create your views here.


def cart(request):
	return render(request , 'store/cart.html')


def add_cart(request):
	product=Product.objects.get(id=product_id)























