from django.db import models
from datetime import datetime

HANDEDNESS = (
    ("LEFT", "Left Handed"),
    ("RIGHT", "Right Handed"),
)

SHOT_HANDEDNESS = (
    ("ONE", "One Handed"),
    ("TWO", "Two Handed"),
)

FORMAT_CHOICES = (
    (1, "Single Set"),
    (3, "Best of 3 Sets"),
    (5, "Best of 5 Sets"),
)

STATUS_CHOICES = (
    ("ABANDONED", "Match Abandoned"),
    ("COMPLETE", "Completed"),
    ("INPROGRESS", "In-Progress"),
)

class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    handedness = models.CharField(max_length=5, choices=HANDEDNESS)
    fh_handedness = models.CharField(max_length=3, choices=SHOT_HANDEDNESS)
    bh_handedness = models.CharField(max_length=3, choices=SHOT_HANDEDNESS)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Match(models.Model):
    players = models.ManyToManyField(Player, related_name='matches_played')
    serving_first = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_served_first')
    format = models.IntegerField(choices=FORMAT_CHOICES)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_won', null=True, blank=True)
    loser = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_lost', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="INPROGRESS")
    location = models.CharField(max_length=100)
    tournament = models.CharField(max_length=100, default="Australian Open")
    date = models.DateField(default=datetime.now)

    def __str__(self):
        players = self.players.all()
        if players.count() == 2:
            return f"{self.tournament} {self.date.strftime('%Y')}: {players[0]} vs {players[1]}"
        return f"{self.tournament} {self.date.strftime('%Y')}"

    @property
    def match_winner(self):
        win_threshold = self.format // 2 + 1
        players = self.players.all()

        win_counts = {player.id: 0 for player in players}
        for s in self.sets.all():
            if s.winner_id:
                win_counts[s.winner_id] += 1
        
        for player in players:
            if win_counts[player.id] >= win_threshold:
                return player

        return None

class Set(models.Model):
    match = models.ForeignKey(Match, related_name='set_scores', on_delete=models.CASCADE)
    number = models.IntegerField()
    winner = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL)
    player1_games = models.IntegerField(default=0)
    player2_games = models.IntegerField(default=0)

    def __str__(self):
        return f"Set {self.number}"
