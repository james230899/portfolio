import datetime

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_title = models.CharField(max_length=50, default="ERROR_MISSING_TITLE")
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    voters = models.ManyToManyField(User, related_name="questions_voted_on", blank=True)
    ranked_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.question_title
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, related_name="choices_voted_on", blank=True)
    date_chosen = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.choice_text
    
class Ranking(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="ranked_choices", blank=True)
    ranked_choices = models.JSONField(null=True)

    class Meta:
        unique_together = ('user','question')

    def __str__(self):
        return f"Ranking by {self.user} for '{self.question}'"
    
class Issue(models.Model):
    issue_title = models.CharField(max_length=50)
    issue_description = models.CharField(max_length=200)

    def __str__(self):
        return self.issue_title

class MonthlyVote(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    month = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('issue', 'month')
        ordering = ['-month']
    
    def __str__(self):
        return f"{self.issue.issue_title} ({self.month.strftime('%B %Y')})"

class MonthlyChoice(models.Model):
    vote_session = models.ForeignKey(MonthlyVote, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, related_name="monthly_choices_voted_on", blank=True)

    def __str__(self):
        return f"{self.choice_text} ({self.vote_session})"