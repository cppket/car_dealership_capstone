from django.contrib import admin
from django.urls import path
from dealership import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("dealer/<int:dealer_id>/", views.dealer_page, name="dealer-page"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("api/csrf/", views.csrf_token_view, name="csrf"),
    path("api/register/", views.register_view, name="register"),
    path("api/dealers/", views.dealers_view, name="dealers"),
    path("api/dealers/state/<str:state>/", views.dealers_by_state_view, name="dealers-by-state"),
    path("api/dealers/<int:dealer_id>/", views.dealer_detail_view, name="dealer-detail"),
    path("api/dealers/<int:dealer_id>/reviews/", views.dealer_reviews_view, name="dealer-reviews"),
    path("api/dealers/<int:dealer_id>/reviews/create/", views.create_review_view, name="create-review"),
    path("api/carmakes/", views.car_makes_view, name="car-makes"),
    path("api/analyze_review/", views.analyze_review_view, name="analyze-review"),
]
