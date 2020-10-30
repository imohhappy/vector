from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.FileField(upload_to='pics', blank=True)
    overview = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.FileField(upload_to='pics')
    overview = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    avaliable = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created', ]

    def get_absolute_url(self):
        return reverse('detail', kwargs={'category_id': self.id, 'pk': self.slug})


class Order(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    postal_code = models.CharField(max_length=4)
    city = models.CharField(max_length=30)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'Order {}'.format(self.id)
