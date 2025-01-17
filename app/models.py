from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
class Category(models.Model):
    subCategory = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subCategories', null=True, blank=True)
    isSub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='produc')
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,blank=True)
    date_order = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.id)
    @property
    def getNumberOfProducts(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    def getTotalAmount(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.getCost for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True ,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True ,blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_add = models.DateField(auto_now_add=True)
    @property
    def getCost(self):
        return self.quantity * self.product.price

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True ,blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    phonenumber = models.CharField(max_length=10, null=True)
    date_add = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.address