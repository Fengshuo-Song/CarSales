from django.dispatch.dispatcher import receiver  # 删除文件
from django.db.models.signals import pre_delete  # 删除文件
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Car(models.Model):
    BODY_STYLE_CHOICES = (
        ('car', 'Car'),
        ('suv', 'SUV'),
        ('truck', 'Pickup Truck'),
        ('van', 'Minivan'),
    )
    FUEL_TYPE_CHOICES = (
        ('gas', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
        ('other', 'Other'),
    )
    DRIVETRAIN_CHOICES = (
        ('AWD', 'All Wheels Drive'),
        ('FWD', 'Front Wheels Drive'),
        ('RWD', 'Rear Wheels Drive'),
        ('4*4', '4*4'),
        ('other', 'Other'),
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    trim = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(default=2020)
    price = models.IntegerField(default=0)

    style = models.CharField(max_length=20,
                             choices=BODY_STYLE_CHOICES)
    fuel_type = models.CharField(max_length=100,
                                 choices=FUEL_TYPE_CHOICES)

    mileage = models.IntegerField(default=0)
    VIN = models.CharField(max_length=20, unique=True)
    owner_name = models.CharField(max_length=100)
    description = models.TextField()

    image = models.ImageField(blank=True, upload_to="car_small_image/")

    exterior_color = models.CharField(max_length=50, default="--")
    interior_color = models.CharField(max_length=50, default="--")
    engine = models.CharField(max_length=50, default="--")
    drivetrain = models.CharField(max_length=20, choices=DRIVETRAIN_CHOICES)
    horsepower = models.IntegerField(default=160)
    displacement = models.FloatField(default="2.0")
    cylinder = models.CharField(max_length=10, default="I4")
    torque = models.IntegerField(default=150)
    seating = models.IntegerField(default=5)
    city_mpg = models.IntegerField(default=30)
    hwy_mpg = models.IntegerField(default=30)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        if self.trim == "":
            return str(self.year) + ' ' + self.brand + ' ' + self.model
        return str(self.year) + ' ' + self.brand + ' ' + self.model + ' ' + self.trim

    def get_absolute_url(self):  # SP!
        return reverse('cars:product_detail', args=(self.VIN,))


class CarImage(models.Model):
    car = models.ForeignKey(Car, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="cars_image/")

    def __str__(self):
        if self.car.trim == "":
            return str(self.car.year) + ' ' + self.car.brand + ' ' + self.car.model
        return str(self.car.year) + ' ' + self.car.brand + ' ' + self.car.model + ' ' + self.car.trim

class Rating(models.Model):
    car = models.ForeignKey(Car, default=None, on_delete=models.CASCADE,
                             related_name='ratings')
    comfort_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    performance_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    safety_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    reliability_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f'Thanks for you rating on {self.car}'

class Comment(models.Model):
    car = models.ForeignKey(Car, default=None, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.car}'

# SP!
# models.py


@receiver(pre_delete, sender=Car)  # sender=你要删除或修改文件字段所在的类**
def download_delete(instance, **kwargs):  # 函数名随意
    print('Car进入文件删除方法，{}删的是{}'.format(instance, instance.image))  # 用于测试
    instance.image.delete(True)  # image是保存文件或图片的字段名**


@receiver(pre_delete, sender=CarImage)  # sender=你要删除或修改文件字段所在的类**
def download_delete(instance, **kwargs):  # 函数名随意
    print('CarImage进入文件删除方法，{}删的是{}'.format(instance, instance.image))  # 用于测试
    instance.image.delete(True)  # image是保存文件或图片的字段名**
