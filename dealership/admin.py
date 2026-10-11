from django.contrib import admin
from .models import Dealer, CarMake, Review

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "state")
    list_filter = ("state",)
    search_fields = ("name", "city", "state")

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("id", "make")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "dealer", "user", "created_at")
    list_filter = ("created_at",)
