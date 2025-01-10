# admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import BibleDb,OldTestamentBook, Chapter,NewTestamentBook,ChapterNew,TaxonomyBibleStudy #,Authormessage

# from django.contrib import admin
# from .models import Authormessage, TaxonomyBibleStudy

# from django.contrib import admin
# from .models import Authormessage, TaxonomyBibleStudy
#########################################################################
# from django.contrib import admin
# from .models import Authormessage, TaxonomyBibleStudy

# class AuthormessageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'select_tag', 'select_book', 'chapter')

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         """
#         Modify the queryset for ForeignKey fields (author and select_tag) to show relevant values.
#         """
#         if db_field.name == "author":
#             # Only show `add_author` in the `author` dropdown
#             kwargs["queryset"] = TaxonomyBibleStudy.objects.all()
#             # Ensure that only add_author is shown in the admin for `author`
#             # kwargs["widget"] = admin.widgets.FilteredSelectMultiple("author", False)
#         elif db_field.name == "select_tag":
#             # Only show `add_taxonomy` in the `select_tag` dropdown
#             kwargs["queryset"] = TaxonomyBibleStudy.objects.all()
#             # Ensure that only add_taxonomy is shown in the admin for `select_tag`
#             # kwargs["widget"] = admin.widgets.FilteredSelectMultiple("select_tag", False)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

# admin.site.register(Authormessage, AuthormessageAdmin)
###############################################################
from .models import TaxonomyBibleStudy,Author,Authormessage

class TaxonomyBibleStudyAdmin(admin.ModelAdmin):
    list_display=('add_taxonomy',)
    search_fields=('add_taxonomy',)

class AuthorAdmin(admin.ModelAdmin):
    list_display=('add_author',)
    search_fields=('add_author',)

class AuthormessageAdmin(admin.ModelAdmin):
    list_display=('title','author',)
    search_fields=('title','author',)

admin.site.register(TaxonomyBibleStudy,TaxonomyBibleStudyAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Authormessage,AuthormessageAdmin)



############################################################
from django.contrib import admin
from .models import  Correction 

class CorrectionAdmin(admin.ModelAdmin):
    list_display = ('bookname', 'chapter', 'versecount',  'created_at', 'resolved')  #'user',
    list_filter = ('resolved', 'bookname', 'chapter')
    search_fields = ('bookname', 'chapter', 'versecount', )  #'user__username'

    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(resolved=True)
    mark_as_resolved.short_description = "Mark selected corrections as resolved"

admin.site.register(Correction, CorrectionAdmin)


############################################################
class BibleDbAdmin(ImportExportModelAdmin):
    list_display = ('book', 'bookname', 'tamilname', 'chapter', 'versecount', 'verse', 'kjv')
    search_fields = ('book', 'bookname', 'tamilname', 'chapter', 'verse')
    list_filter = ('book', 'chapter')

# class TaxonomyBibleStudyAdmin(admin.ModelAdmin):
#     list_display = ('add_taxonomy', 'add_author')
#     search_fields = ('add_taxonomy', 'add_author')

# admin.site.register(TaxonomyBibleStudy, TaxonomyBibleStudyAdmin)

# class AuthormessageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'url','author','select_tag','select_book','chapter',)#'tamil_bible_message')
#     search_fields = ('title', 'select_book','chapter')

# admin.site.register(Authormessage, AuthormessageAdmin)





class OldTestamentBookAdmin(admin.ModelAdmin):
    list_display = ('bookname','booknametamil','totalchapters')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'chapter_number')

class NewTestamentBookAdmin(admin.ModelAdmin):
    list_display = ('bookname','booknametamil','totalchapters')

class ChapterNewAdmin(admin.ModelAdmin):
    list_display = ('booknew', 'newchapter_number')


# from django.contrib import admin
from .models import dailyverse_day

@admin.register(dailyverse_day)
class DailyVerseAdmin(admin.ModelAdmin):
    list_display = ('date', 'tamilname', 'chapter', 'versecount', 'verse', 'kjv')
    search_fields = ('date', 'tamilname')
    list_filter = ('date',)

from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from .models import Verse_of_the_day,Daily_bible_reading

class VerseOfTheDayAdmin(admin.ModelAdmin):
    list_display = ('date','bookname', 'tamilname', 'chapter', 'versecount', 'verse', 'kjv')
    search_fields = ('date','bookname', 'chapter', 'versecount')
    list_filter = ('bookname', 'date')
    ordering = ('date',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        # Get the current date and the date 60 days ahead
        today = make_aware(datetime.today())
        end_date = today + timedelta(days=60)

        # Return only the records from today to 60 days from today
        return super().get_queryset(request).filter(date__range=[today.date(), end_date.date()])

admin.site.register(Verse_of_the_day, VerseOfTheDayAdmin)

class DailyBibleReading(admin.ModelAdmin):
    list_display = ('date','bookname', 'tamilname', 'chapter')
    search_fields = ('date','bookname', 'chapter')
    list_filter = ('bookname', 'date')
    ordering = ('date',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        # Get the current date and the date 60 days ahead
        today = make_aware(datetime.today())
        end_date = today + timedelta(days=60)

        # Return only the records from today to 60 days from today
        return super().get_queryset(request).filter(date__range=[today.date(), end_date.date()])

admin.site.register(Daily_bible_reading,DailyBibleReading)


admin.site.register(BibleDb, BibleDbAdmin)
admin.site.register(OldTestamentBook, OldTestamentBookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(NewTestamentBook, NewTestamentBookAdmin)
admin.site.register(ChapterNew, ChapterNewAdmin)
