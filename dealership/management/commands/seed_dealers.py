from django.core.management.base import BaseCommand
from dealership.models import Dealer, CarMake

class Command(BaseCommand):
    help = "Create sample dealership and car make data for local development."

    def handle(self, *args, **options):
        sample_dealers = [
            ("Prairie Auto Center", "100 Main Street", "Wichita", "Kansas", "67202", "316-555-0101"),
            ("Sunflower Motors", "25 Market Avenue", "Topeka", "Kansas", "66603", "785-555-0102"),
            ("Metro Car House", "80 Oak Road", "Overland Park", "Kansas", "66204", "913-555-0103"),
            ("Lakeside Auto", "14 Lake Drive", "Chicago", "Illinois", "60601", "312-555-0104"),
            ("Mountain View Cars", "9 Pine Street", "Denver", "Colorado", "80202", "303-555-0105"),
        ]
        for name, address, city, state, zip_code, phone in sample_dealers:
            Dealer.objects.get_or_create(name=name, defaults={
                "address": address, "city": city, "state": state, "zip_code": zip_code, "phone": phone
            })
        makes = {
            "Toyota": ["Camry", "Corolla", "RAV4"],
            "Honda": ["Civic", "Accord", "CR-V"],
            "Ford": ["Mustang", "Escape", "F-150"],
            "BMW": ["3 Series", "5 Series", "X5"],
            "Tesla": ["Model 3", "Model Y", "Model S"],
        }
        for make, models in makes.items():
            CarMake.objects.get_or_create(make=make, defaults={"models": models})
        self.stdout.write(self.style.SUCCESS("Sample dealerships and car makes are ready."))
