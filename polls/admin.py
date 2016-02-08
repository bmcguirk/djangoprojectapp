from django.contrib import admin
from .models import Question, Choice


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("The Question", {'fields':['question_text']}),
        ("Date Information",{'fields':['pub_date'],
                             'classes':['collapse']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date','was_published_recently')
    list_filter = ['pub_date']
    search_fields = ["question_text"]

admin.site.site_title = "Polls Administration"
admin.site.site_header = "Polls Administration"
admin.site.index_title = "App Administration"
admin.site.register(Question, QuestionAdmin)

# Register your models here.
