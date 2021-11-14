from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
	product_name = models.CharField(max_length=200,unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(max_length=1000, blank=True)
	price = models.IntegerField()
	images = models.ImageField(upload_to='photos/products')
	stock = models.IntegerField()
	is_available = models.BooleanField(default=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
	actual_price = models.IntegerField(blank=True,default=0)

	def get_url(self):
		return reverse('product_detail', args=[self.category.slug, self.slug])
	    # now to use in template we will use {{ product.get_url }}

	def __str__(self):
		return self.product_name


