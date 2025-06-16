from django.db import models

# Create your models here.
class Product(models.Model):
    CAT=((1,"Fruits & Vegetables "),(2,"Pulses & Cereals"),(3,"Farming Tools and Equipements"),(4,"Dairy Products"),(5,"Herbs"),(6,"Nursery & Plants"))
    pname=models.CharField(max_length=60)
    price=models.IntegerField()
    description=models.CharField(max_length=200)
    category=models.IntegerField(choices=CAT)
    is_available=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='image')

    def __str__(self):
        return self.pname
    
class Cart(models.Model):
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Address(models.Model):
    user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE,db_column="user_id")
    address=models.CharField(max_length=200)
    fullname=models.CharField(max_length=50)
    city=models.CharField(max_length=40)
    pincode=models.CharField(max_length=10)
    state=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE, db_column="user_id")
    p_id=models.ForeignKey("product",on_delete=models.CASCADE, db_column="p_id")
    qty=models.IntegerField(default=1)
    amt=models.FloatField()
    payment_status=models.CharField(max_length=30,default="unpaid")


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='default-profile.png')

    def __str__(self):
        return f"{self.user.username}'s profile"