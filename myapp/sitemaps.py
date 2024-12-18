from django.contrib.sitemaps import Sitemap
from django.urls  import reverse
from .models import BibleDb
from django.utils.text import slugify
from datetime import datetime





class StaticViewSitemap(Sitemap):


    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['index','book_list']


    def location(self, item):
        return reverse(item)






# class bibleSitemap(Sitemap):

#     def items(self):
#         return BibleDb.objects.all()


#     def location(self,obj):
#          url=obj.url
#          bookname=obj.bookname
#          chapter=obj.chapter
#          versecount=obj.versecount
#          return '/tamil/%s/%s/%s' %((bookname,chapter,versecount))
