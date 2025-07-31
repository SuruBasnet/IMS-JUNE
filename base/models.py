from django.db import models

# Create your models here.
class ProductType(models.Model):
    name = models.CharField(max_length=300)

class Department(models.Model):
    name = models.CharField(max_length=300)

class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    stock = models.IntegerField()
    type = models.ForeignKey(ProductType,on_delete=models.SET_NULL, null=True)
    department = models.ManyToManyField(Department)


class Vendor(models.Model):
    name = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

class Purchase(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField()
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Customer(models.Model):
    name = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)

class Sell(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='sells')
    # type = models.ForeignKey(ProductType) # To define which type of product is being selled (Not ideal becasue product is related as per requirement and type is related on product so we can directly use product relation to get type value aswell)
    price = models.FloatField()
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()