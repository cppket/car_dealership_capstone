import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Dealer, CarMake, Review

class DealershipAPITests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.dealer = Dealer.objects.create(
            name="Kansas Auto", address="1 Main Street", city="Wichita",
            state="Kansas", zip_code="67202"
        )
        CarMake.objects.create(make="Toyota", models=["Camry", "Corolla"])
        self.user = User.objects.create_user(username="testuser", password="Test-pass-123", email="test@example.com")

    def test_list_dealers(self):
        response = self.client.get("/api/dealers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["dealers"]), 1)

    def test_dealer_detail(self):
        response = self.client.get(f"/api/dealers/{self.dealer.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["dealer"]["name"], "Kansas Auto")

    def test_filter_kansas(self):
        response = self.client.get("/api/dealers/state/Kansas/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["dealers"]), 1)

    def test_reviews(self):
        Review.objects.create(dealer=self.dealer, user=self.user, review="Fantastic services")
        response = self.client.get(f"/api/dealers/{self.dealer.id}/reviews/")
        self.assertEqual(len(response.json()["reviews"]), 1)

    def test_car_makes(self):
        response = self.client.get("/api/carmakes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["car_makes"][0]["make"], "Toyota")

    def test_sentiment(self):
        response = self.client.post("/api/analyze_review/", data=json.dumps({"review":"Fantastic services"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment"], "positive")

    def test_register(self):
        response = self.client.post("/api/register/", data=json.dumps({
            "username":"newuser", "first_name":"New", "last_name":"User",
            "email":"new@example.com", "password":"Another-pass-123"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_logout(self):
        response = self.client.post("/accounts/login/", {"username":"testuser", "password":"Test-pass-123"})
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/accounts/logout/")
        self.assertEqual(response.status_code, 200)

    def test_review_requires_login(self):
        response = self.client.post(
            f"/api/dealers/{self.dealer.id}/reviews/create/",
            data=json.dumps({"review":"Nice service"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_authenticated_review_creation(self):
        self.client.force_login(self.user)
        response = self.client.post(
            f"/api/dealers/{self.dealer.id}/reviews/create/",
            data=json.dumps({"review":"Great service"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)
