from django.conf import settings
from django.db import models

class Dealer(models.Model):
    name = models.CharField(max_length=160)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, db_index=True)
    zip_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state})"

class CarMake(models.Model):
    make = models.CharField(max_length=100)
    models = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.make

class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dealer_reviews")
    name = models.CharField(max_length=120, blank=True)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review for {self.dealer_id} by {self.user.username}"
