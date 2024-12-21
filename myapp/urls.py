from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf.urls.static import static
from django.conf import settings
from myapp.sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap




sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [


path('', views.index, name='index'),
# path('', views.get_daily_verse, name='index'),
#path('get-translation/<int:verse_id>/', views.get_translation, name='get_translation'),
path('base', views.base, name='base'),
path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
path('tamil2/<str:bookname>/<str:chapter>/<str:versecount>',views.verse,name='verse'),
path('response', views.response, name='response'),
path('base_english', views.base_english, name='base_english'),
path('song_list', views.song_list, name='song_list'),
#path('chapter/<str:bookname>/<str:chapter>', views.chapter_detail, name='chapter_detail'),
path('tamill/<str:bookname>/<str:chapter>/', views.chapter2, name='chapter2'),
path('englishh/<str:bookname>/<str:chapter>/', views.chapter3, name='chapter3'),
path('bible-search/', views.bible_search, name='bible_search'),
path('tamil/<str:bookname>/<str:chapter>/', views.chapter_detail, name='chapter_detail'),
path('tamil/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_detail,name='verse_detail'),
path('tamilenglish/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_detail2,name='verse_detail2'),
path('tamil/', views.book_list, name='book_list'),  # URL to render the book list
path('english/',views.book_list_english,name='book_list_english'),
path('english/<str:bookname>/<str:chapter>/', views.chapter_detail_english, name='chapter_detail_english'),
path('english/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_detail_english,name='verse_detail_english'),
path('englishtamil/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_detail3,name='verse_detail3'),
path('get-chapters/<str:bookname>/', views.get_chapters, name='get_chapters'),  # API for fetching chapters
# path('cermon/',views.cermon_view,name='cermon'),
# Add a dynamic URL for BibleReferences
path('tamil-bible-message/<str:url>/', views.cermon_view, name='cermon_detail'),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
