from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("ranked_choices/", views.ranked_choices, name="ranked_choices"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    path("<int:question_id>/", views.question_detail, name="detail"),
    path("<int:question_id>/results/", views.question_result, name="results"),
    path("<int:question_id>/results_ranked/", views.question_result_ranked, name="results_ranked"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/vote_ranked/", views.vote_ranked, name="vote_ranked"),
]