from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [


path('', views.index, name='index'),
path('tamil-bible-study', views.tamil_bible_study, name='tamil-bible-study'),
#path('get-translation/<int:verse_id>/', views.get_translation, name='get_translation'),
path('base', views.base, name='base'),
path('tamil2/<str:bookname>/<str:chapter>/<str:versecount>',views.verse,name='verse'),
path('english2/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_english,name='verse_english'),
path('response', views.response, name='response'),
path('base_english', views.base_english, name='base_english'),
# path('song_list', views.song_list, name='song_list'),
#path('chapter/<str:bookname>/<str:chapter>', views.chapter_detail, name='chapter_detail'),
path('tamill/<str:bookname>/<str:chapter>/', views.chapter2, name='chapter2'),
path('englishh/<str:bookname>/<str:chapter>/', views.chapter3, name='chapter3'),
#path('bible-search/', views.bible_search, name='bible_search'),
path('search/', views.search_bible, name='search_bible'),
path('tamil/<str:bookname>/<str:chapter>/', views.chapter_detail, name='chapter_detail'),
path('tamil/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_detail,name='verse_detail'),
path('tamilenglish/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_detail2,name='verse_detail2'),
path('tamil/', views.book_list, name='book_list'),  # URL to render the book list
path('english/',views.book_list_english,name='book_list_english'),
path('english/<str:bookname>/<str:chapter>/', views.chapter_detail_english, name='chapter_detail_english'),
path('english/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_detail_english,name='verse_detail_english'),
path('englishtamil/<str:bookname>/<str:chapter>/<str:versecount>',views.verse_detail3,name='verse_detail3'),
path('get-chapters/<str:bookname>/', views.get_chapters, name='get_chapters'),  # API for fetching chapters
path('tamil/verse/search/<str:word>/', views.verse_detail_by_word, name='verse_detail_by_word'), # New URL pattern for searching by word
path('english/verse/search/<str:word>/',views.verse_detail_by_wordenglish,name='verse_detail_by_wordenglish'),
path('tamil-bible-message/<str:url>/', views.sermon_view, name='sermon_detail'),
path('tamil/<str:bookname>/<str:chapter>/<str:startverse>-<str:endverse>/', views.verse_detail_range, name='verse_detail_range'),  # For verse range
path('search_present', views.search_form, name='search_form'),  # Primary tab
    path('verse_present/', views.verse_present, name='verse_present'),  # Secondary tab
    path('get-chapters/<str:bookname>/', views.get_chapters, name='get_chapters'),
    path('get-versecounts/<str:bookname>/<str:chapter>/', views.get_versecounts, name='get_versecounts'),
    path('get-verse-details/<str:bookname>/<str:chapter>/<str:versecount>/', views.get_verse_details, name='get_verse_details'),
    path('set_fullscreen', views.set_fullscreen, name='set_fullscreen'),
    path('fullscreen/', views.fullscreen_view, name='fullscreen_page'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
