from django.shortcuts import render


def home(request):
	# print('request jo aa rhi hai vo:',request)
	return render(request,'home.html')