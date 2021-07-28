from django.contrib import admin

from .models import Car, CarImage

class CarImageAdmin(admin.StackedInline):
    model = CarImage

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageAdmin]
    class Meta:
        model = Car

    list_display = ('brand', 'model', 'year', 'price', 'mileage','style')
    list_filter = ('brand', 'year','fuel_type',)
    search_fields = ('brand', 'model',)

    ordering = ('year',)

# @admin.register(CarImageAdmin)

class CarImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(CarImage, CarImageAdmin)