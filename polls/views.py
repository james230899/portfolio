from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db import IntegrityError
from django.views.decorators.http import require_POST
import pprint

# Login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *
from collections import Counter

# Finds duplicates in ranked_choice
def has_duplicates(items):
    return len(items) != len(set(items))

def index(request):
    question_list = Question.objects.filter(ranked_choice=False).order_by("-pub_date")
    return render(request, "polls/index.html", {
        'title': 'Question List',
        'question_list': question_list,
    })

def ranked_choices(request):
    question_list = Question.objects.filter(ranked_choice=True).order_by("-pub_date")
    return render(request, "polls/index.html", {
        'title': 'Ranked Choice Questions',
        'question_list': question_list,
    })

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()

    has_voted = request.user.is_authenticated and question.voters.filter(id=request.user.id).exists()
    

    was_chosen = None
    if has_voted:
        try:
            was_chosen = choices.filter(voters=request.user)
        except Choice.DoesNotExist:
            pass
    
    ranked_choice_texts = None

    if question.ranked_choice:
        template = "polls/detail_ranked.html"
        if has_voted:
            ranking = Ranking.objects.get(user=request.user, question=question)
            choices = question.choice_set.all()
            choice_map = {choice.id: choice.choice_text for choice in choices}
            ranked_choice_texts = [choice_map.get(cid, "Unknown Choice") for cid in ranking.ranked_choices]
    else:
        template = "polls/detail.html"

    return render(request, template, {
        "question": question,
        "choices": choices,
        "has_voted": has_voted,
        "was_chosen": was_chosen,
        "ranking": ranked_choice_texts,
    })

def question_result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    data = [choice.votes for choice in choices]
    labels = [choice.choice_text for choice in choices]
    no_results = not any(choice.votes > 0 for choice in choices)
    max_votes = max((choice.votes for choice in choices), default=0)

    return render(request, "polls/results.html", {
        "question": question,
        "data": data,
        "labels": labels,
        "no_results": no_results,
        "max_votes": max_votes,
    })

def question_result_ranked(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    no_results = (not any(choice.votes > 0 for choice in choices) or not request.user.is_authenticated)
    max_votes = max((choice.votes for choice in choices), default=0)
    
    try:
        ranking = Ranking.objects.get(user=request.user, question=question)
    except Ranking.DoesNotExist:
        return render(request, "polls/results_ranked.html", {
            "question": question,
            "ranking": None,
            "error_message": "You have not voted in this poll.",
            "no_results": no_results,
        })
    except TypeError:
        return render(request, "polls/results_ranked.html", {
            "question": question,
            "ranking": None,
            "no_results": True,
        })

    # Resolve choice IDs to choice texts
    choices = question.choice_set.all()
    choice_map = {choice.id: choice.choice_text for choice in choices}
    ranked_choice_texts = [choice_map.get(cid, "Unknown Choice") for cid in ranking.ranked_choices]

    # Rank choices by number of votes
    votes_dict = {
        choice.choice_text: choice.votes
            for choice in sorted(choices, key=lambda c: c.votes, reverse=True)
    }

    # Get data and labels
    data = list(votes_dict.values())
    labels = list(votes_dict.keys())



    return render(request, "polls/results_ranked.html", {
        "question": question,
        "ranking": ranked_choice_texts,
        "data": data,
        "labels": labels,
        "error_message": None,
        "no_results": no_results,
        "votes_dict": votes_dict,
        "max_votes": max_votes,
    })

@require_POST
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user.is_authenticated:
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.voters.add(request.user)
            selected_choice.save()
            question.voters.add(request.user)

            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    else:
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You must be logged in to vote in this poll",
            },
        )

@require_POST
def vote_ranked(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    
    if request.user.is_authenticated:
        ranked_choices = []
        i = 0

        while True:
            key = f"ranked_choice_{i}"
            choice_id = request.POST.get(key)

            if choice_id is None:
                break

            ranked_choices.append(int(choice_id))
            i += 1

        # Check if a choice was ranked twice
        if has_duplicates(ranked_choices):
            return render(request, "polls/detail_ranked.html", {
                "question": question,
                "error_message": "You cannot rank the same choice more than once.",
            })


        for index, choice in enumerate(ranked_choices, 0):
            try:
                selected_choice = question.choice_set.get(pk=choice)
            except (KeyError, Choice.DoesNotExist):
                # Redisplay the question voting form.
                return render(
                    request,
                    "polls/detail_ranked.html",
                    {
                        "question": question,
                        "error_message": "You didn't select a choice.",
                    },
                )
            else:
                selected_choice.votes = F("votes") + (len(ranked_choices) - index)
                selected_choice.voters.add(request.user)
                selected_choice.save()

        Ranking.objects.create(
            question=question,
            user=request.user,
            ranked_choices=ranked_choices,
        )
        question.voters.add(request.user)
        
        return HttpResponseRedirect(reverse("polls:results_ranked", args=(question.id,)))
    
    else:
        return render(
            request,
            "polls/detail_ranked.html",
            {
                "question": question,
                "error_message": "You must be logged in to vote in this poll",
            },
        )

# Login
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("polls:index"))
        else:
            return render(request, "polls/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "polls/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("polls:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "polls/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "polls/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "polls/register.html")