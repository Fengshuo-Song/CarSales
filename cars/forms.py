from django import forms

from cars.models import Car, Comment, Rating


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand','model','trim','year','price','style','fuel_type',
        'mileage','VIN','owner_name','description', 'image', 'exterior_color',
        'interior_color','engine','drivetrain','horsepower','displacement',
        'cylinder','torque','seating','city_mpg','hwy_mpg']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['comfort_rating','performance_rating','safety_rating',
        'reliability_rating']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
