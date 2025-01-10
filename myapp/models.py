from django.db import models

class BibleDb(models.Model):
    book = models.CharField(max_length=100)
    bookname = models.CharField(max_length=100)
    tamilname = models.CharField(max_length=10)
    chapter = models.CharField(max_length=100)  # Format "1:1", "2:10", etc.
    versecount = models.CharField(max_length=100)
    verse = models.TextField()
    kjv = models.TextField()

class OldTestamentBook(models.Model):
    bookname = models.CharField(max_length=100)
    booknametamil=models.CharField(max_length=100,null=True)
    totalchapters=models.IntegerField(null=True)
    def __str__(self):
        return self.bookname# models.py

class Chapter(models.Model):
    book = models.ForeignKey(OldTestamentBook, on_delete=models.CASCADE)
    chapter_number = models.IntegerField() 
    def __str__(self):
        return f"{self.book.bookname} Chapter {self.chapter_number}"    
    
class NewTestamentBook(models.Model):
    bookname = models.CharField(max_length=100)
    booknametamil=models.CharField(max_length=100,null=True)
    totalchapters=models.IntegerField(null=True)
    def __str__(self):
        return self.bookname

class ChapterNew(models.Model):
    booknew = models.ForeignKey(NewTestamentBook, on_delete=models.CASCADE) 
    newchapter_number = models.IntegerField()  

    def __str__(self):
        return f"{self.booknew.bookname} Chapter {self.newchapter_number}" 

####################### for daily verse
from django.db import models

class DailyVerse(models.Model):
    date = models.DateField(unique=True)
    verse = models.ForeignKey(BibleDb, on_delete=models.CASCADE)

    def __str__(self):
        return f"Verse for {self.date}: {self.verse}"
    

##################### for old dailyverse
class dailyverse_day(models.Model):
    date=models.DateField(unique=True)
    tamilname = models.CharField(max_length=10)
    chapter = models.IntegerField()
    versecount = models.IntegerField()
    verse = models.TextField()
    kjv = models.TextField()

################### verse of the day
class Verse_of_the_day(models.Model):
    date=models.DateField(unique=True)
    bookname=models.CharField(max_length=20)
    tamilname=models.CharField(max_length=20)
    chapter=models.IntegerField()
    versecount=models.IntegerField()
    verse=models.TextField()
    kjv=models.TextField()

class Daily_bible_reading(models.Model):
    date=models.DateField(unique=True)
    bookname=models.CharField(max_length=20)
    tamilname=models.CharField(max_length=20)
    chapter=models.IntegerField()

from django.db import models
#from ckeditor.fields import RichTextField  # Importing RichTextField from ckeditor

# class TaxonomyBibleStudy(models.Model):
#     add_taxonomy = models.CharField(max_length=200)
#     add_author = models.CharField(max_length=100)

#     def __str__(self):
#         # For displaying `add_author` in the `author` dropdown and `add_taxonomy` in the `select_tag` dropdown
#         return f"{self.add_author} - {self.add_taxonomy}"

from django.db import models
from ckeditor.fields import RichTextField  # Ensure you have CKEditor installed if using RichTextField

class TaxonomyBibleStudy(models.Model):
    add_taxonomy = models.CharField(max_length=200)

    def __str__(self):
        return self.add_taxonomy


class Author(models.Model):
    add_author = models.CharField(max_length=100)

    def __str__(self):
        return self.add_author


class Authormessage(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='bible_references')
    select_tag = models.ForeignKey(TaxonomyBibleStudy, on_delete=models.CASCADE, related_name='selected_tags')
    # select_book = models.CharField(max_length=100)
    # bookname=models.CharField(max_length=100)
    # chapter = models.IntegerField()
    # Uncomment the following line if you want to use RichTextField
    tamil_bible_message = RichTextField(null=True, blank=True)

    def __str__(self):
        return f"{self.author.add_author} - Title: {self.title}"


###################################################

from django.db import models

class Correction(models.Model):
    bookname = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    versecount = models.CharField(max_length=100)
    #user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming user is logged in
    suggested_correction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)  # To track if the issue is resolved

    def __str__(self):
        return f"Correction for {self.bookname} {self.chapter}:{self.versecount}"
    



