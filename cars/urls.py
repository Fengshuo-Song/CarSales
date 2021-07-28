from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('list/', views.CarListView.as_view(), name='car_list'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('search/', views.search_view, name='search'),
    path('reset/', views.CarReset, name='car_reset'),
    path('rating/<int:pk>/', views.RateView.as_view(), name='car_rate'),
    path('create/', views.CarCreateView.as_view(), name='car_create'),
    path('update/<int:pk>/', views.CarUpdateView.as_view(), name='car_update'),
    path('delete/<int:pk>/', views.CarDeleteView.as_view(), name='car_delete'),
    path('<slug:vin>/', views.product_detail, name='product_detail'),
    path('<slug:vin>/add', views.addPhoto, name='add_photo')

]
