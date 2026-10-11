import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.middleware.csrf import get_token
from .models import Dealer, CarMake, Review

def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

def _dealer_dict(dealer):
    return {
        "id": dealer.id, "name": dealer.name, "address": dealer.address,
        "city": dealer.city, "state": dealer.state, "zip_code": dealer.zip_code,
        "phone": dealer.phone, "website": dealer.website,
    }

def _review_dict(review):
    return {
        "id": review.id, "dealer_id": review.dealer_id, "name": review.name or review.user.username,
        "username": review.user.username, "review": review.review,
        "purchase": review.purchase, "created_at": review.created_at.isoformat(),
    }

@ensure_csrf_cookie
def home(request):
    dealers = Dealer.objects.all().order_by("name")
    return render(request, "home.html", {"dealers": dealers})

def about(request):
    return redirect("/static/About.html")

def contact(request):
    return redirect("/static/Contact.html")

def dealer_page(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    return render(request, "dealer.html", {"dealer": dealer, "reviews": dealer.reviews.all()})

@require_GET
def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

@csrf_protect
@require_POST
def login_view(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid username or password."}, status=400)
    login(request, user)
    return JsonResponse({"message": "Login successful.", "username": user.username})

@csrf_protect
@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logout successful."})

@csrf_protect
@require_POST
def register_view(request):
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    required = ["username", "first_name", "last_name", "email", "password"]
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        return JsonResponse({"error": "Missing required fields.", "fields": missing}, status=400)
    if User.objects.filter(username=data["username"]).exists():
        return JsonResponse({"error": "Username already exists."}, status=400)
    if User.objects.filter(email=data["email"]).exists():
        return JsonResponse({"error": "Email already exists."}, status=400)
    user = User.objects.create_user(
        username=data["username"], first_name=data["first_name"],
        last_name=data["last_name"], email=data["email"], password=data["password"]
    )
    return JsonResponse({"message": "Registration successful.", "username": user.username}, status=201)

@require_GET
def dealers_view(request):
    return JsonResponse({"dealers": [_dealer_dict(d) for d in Dealer.objects.all().order_by("id")]})

@require_GET
def dealers_by_state_view(request, state):
    dealers = Dealer.objects.filter(state__iexact=state).order_by("id")
    return JsonResponse({"state": state, "dealers": [_dealer_dict(d) for d in dealers]})

@require_GET
def dealer_detail_view(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    return JsonResponse({"dealer": _dealer_dict(dealer)})

@require_GET
def dealer_reviews_view(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    return JsonResponse({"dealer_id": dealer.id, "reviews": [_review_dict(r) for r in dealer.reviews.select_related("user")]})

@csrf_protect
@require_POST
def create_review_view(request, dealer_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required."}, status=401)
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    text = str(data.get("review", "")).strip()
    if not text:
        return JsonResponse({"error": "Review text is required."}, status=400)
    review = Review.objects.create(
        dealer=dealer, user=request.user, name=request.user.get_full_name(),
        review=text, purchase=bool(data.get("purchase", False))
    )
    return JsonResponse({"message": "Review added.", "review": _review_dict(review)}, status=201)

@require_GET
def car_makes_view(request):
    return JsonResponse({"car_makes": [{"id": m.id, "make": m.make, "models": m.models} for m in CarMake.objects.all().order_by("make")]})

@require_POST
def analyze_review_view(request):
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    text = str(data.get("review", data.get("text", ""))).strip()
    if not text:
        return JsonResponse({"error": "Review text is required."}, status=400)
    # Lightweight lexical sentiment baseline; replace with the course's required analyzer if specified.
    positive = {"fantastic", "great", "excellent", "good", "amazing", "wonderful", "friendly", "helpful", "love", "best", "awesome", "fast"}
    negative = {"bad", "poor", "terrible", "awful", "worst", "slow", "rude", "hate", "horrible", "disappointing"}
    words = {w.strip(".,!?;:()[]{}").lower() for w in text.split()}
    score = len(words & positive) - len(words & negative)
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return JsonResponse({"review": text, "sentiment": sentiment, "score": score})
