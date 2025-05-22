from django.contrib import admin
from .models import Question, Choice, Ranking

class ChoiceInline(admin.TabularInline):  # or use admin.StackedInline if you prefer
    model = Choice
    extra = 1  # Number of empty choices shown by default
    fields = ('choice_text', 'votes')
    can_delete = True
    show_change_link = True

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'pub_date', 'ranked_choice')
    filter_horizontal = ('voters',)
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes', 'date_chosen')
    list_filter = ('question',)
    search_fields = ('choice_text',)
    list_editable = ('votes',)

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('question', 'user')
    search_fields = ('user__username', 'question__question_text')
