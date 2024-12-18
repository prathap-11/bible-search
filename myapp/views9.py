#views.py
from django.shortcuts import render, redirect
from .models import BibleDb,OldTestamentBook,NewTestamentBook





from django.shortcuts import render
from .models import BibleDb

def bible_search(request):
    tamil_search_query = request.GET.get('tamil_search', '')
    english_search_query = request.GET.get('english_search', '')
    whole_bible = request.GET.get('whole_bible', False)
    selected_book = request.GET.get('book', '')

    # Initialize the query set
    verses = BibleDb.objects.all()

    # Filter based on Tamil search query
    if tamil_search_query:
        verses = verses.filter(verse__icontains=tamil_search_query)
    
    # Filter based on English search query
    if english_search_query:
        verses = verses.filter(verse__icontains=english_search_query)

    # Whole Bible search logic (if enabled)
    if whole_bible:
        verses = verses.all()  # No extra filter needed

    # Filter by selected book (if any)
    if selected_book:
        verses = verses.filter(bookname=selected_book)

    # List of books for dropdown
    books = BibleDb.objects.values_list('bookname', flat=True).distinct()

    return render(request, 'bible_search.html', {
        'verses': verses,
        'tamil_search_query': tamil_search_query,
        'english_search_query': english_search_query,
        'books': books,
        'selected_book': selected_book,
        'whole_bible': whole_bible,
    })




from django.shortcuts import render
from .models import BibleDb


def response(request):
    books = BibleDb.objects.values('tamilname').distinct()
    tamilbook=BibleDb.objects.filter(bookname=bookname).first()
    book=tamilbook.tamilname
    chapter=chapter
    # Get the verses related to the selected chapter
    verses = BibleDb.objects.filter(bookname=bookname,chapter=chapter)
    return render(request,'response.html',{"verses":verses,"books":books,"book":book,"chapter":chapter,"bookname": bookname})



from django.http import HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from .models import BibleDb

# View for displaying all books (song names) with a dynamic chapter load
def book_list(request):
    books = BibleDb.objects.values('tamilname').distinct()
    old_test=OldTestamentBook.objects.all()
    new_test=NewTestamentBook.objects.all()
    bookschapter=[]
    for i in old_test:
        bookschapter.append(i.booknametamil)
    for j in new_test:
        bookschapter.append(j.booknametamil)
    books = BibleDb.objects.values('book', 'bookname', 'tamilname').distinct()
    oldbook=OldTestamentBook.objects.all()
    newbook=NewTestamentBook.objects.all()
    oldbook_with_chapters = []
    for book in oldbook:
        chapters = range(1, book.totalchapters + 1)
        oldbook_with_chapters.append({
            'book': book,
            'chapters': chapters
        })
    newbook_with_chapters=[]
    for book in newbook:
        chapters=range(1,book.totalchapters+1)
        newbook_with_chapters.append({
            'book': book,'chapters': chapters
        })
    # Prepare breadcrumbs
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Tamil Bible / Select Chapter', 'url': '/tamil/'}
    ]
    
    return render(request, 'book_list.html', {'breadcrumbs':breadcrumbs,'oldbook_with_chapters': oldbook_with_chapters,'newbook_with_chapters': newbook_with_chapters,"bookschapter":bookschapter, 'books':books })




#view for display books list in english
def book_list_english(request):
    books = BibleDb.objects.values('bookname').distinct()
    oldbook=OldTestamentBook.objects.all()
    newbook=NewTestamentBook.objects.all()
    oldbook_with_chapters = []
    for book in oldbook:
        chapters = range(1, book.totalchapters + 1)
        oldbook_with_chapters.append({
            'book': book,
            'chapters': chapters
        })
    newbook_with_chapters=[]
    for book in newbook:
        chapters=range(1,book.totalchapters+1)
        newbook_with_chapters.append({
            'book': book,'chapters': chapters
        })
    old_test=OldTestamentBook.objects.all()
    new_test=NewTestamentBook.objects.all()
    bookschapter=[]
    for i in old_test:
        bookschapter.append(i.bookname)
    for j in new_test:
        bookschapter.append(j.bookname)
    # Breadcrumbs logic
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Bible', 'url': '/books/english/'}
    ]
    return render(request, 'book_listenglish.html', {'breadcrumbs':breadcrumbs,'oldbook_with_chapters': oldbook_with_chapters,'newbook_with_chapters': newbook_with_chapters,"bookschapter":bookschapter,"books": books})




# API view to get chapters for a specific book
def get_chapters(request, bookname):
    chapters = BibleDb.objects.filter(bookname=bookname).values('chapter').distinct()
    chapter_list = [chapter['chapter'] for chapter in chapters]
    return JsonResponse({'chapters': chapter_list})



from django.urls import reverse

def base(request):
    books = BibleDb.objects.values('tamilname').distinct()  # Get all distinct book names
    book = request.GET.get('book')
    chapter = request.GET.get('chapter')
    versecount = request.GET.get('versecount')

    breadcrumbs = [{'name': 'Home', 'url': reverse('base')}]

    if book:
        englishbook = BibleDb.objects.filter(tamilname=book).first()
        bookname = englishbook.bookname if englishbook else None
        breadcrumbs.append({'name': book, 'url': f'?book={book}'})  # Link for the selected book

        if chapter:
            breadcrumbs.append({'name': f'Chapter {chapter}', 'url': f'?book={book}&chapter={chapter}'})  # Link for the selected chapter

            if versecount:
                breadcrumbs.append({'name': f'Verse {versecount}', 'url': f'?book={book}&chapter={chapter}&versecount={versecount}'})  # Link for the selected verse

                # Get the current verse details based on bookname, chapter, and versecount
                verse_details = BibleDb.objects.filter(tamilname=book, chapter=chapter, versecount=versecount)
                if verse_details.exists():
                    current_verse = verse_details.first()

                    # Get the previous and next verses based on the ID
                    previous_verse = BibleDb.objects.filter(id__lt=current_verse.id, tamilname=book, chapter=chapter).order_by('-id').first()
                    next_verse = BibleDb.objects.filter(id__gt=current_verse.id, tamilname=book, chapter=chapter).order_by('id').first()

                    return render(request, 'verse_detail.html', {
                        'book': book,
                        'bookname': bookname,
                        'chapter': chapter,
                        'versecount': versecount,
                        'verse_details': verse_details,
                        'books': books,
                        'breadcrumbs': breadcrumbs,
                        'previous_verse': previous_verse,
                        'next_verse': next_verse,
                    })

            else:
                # If no versecount is provided, render chapter_detail.html
                verses = BibleDb.objects.filter(tamilname=book, chapter=chapter)
                current_book = book
                print('current_book',current_book)
                next_book=book   
                prev_book=book
                
            
                # Get all chapters of the current book
                all_chapters = BibleDb.objects.filter(tamilname=current_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))
                print('chapter',chapter)
                print('all chapters',all_chapters)
                # Find index of current chapter
                chapter_index = list(all_chapters).index(chapter)
                
                # Determine previous and next chapters
                prev_chapter = all_chapters[chapter_index - 1] if chapter_index > 0 else None
                next_chapter = all_chapters[chapter_index + 1] if chapter_index < len(all_chapters) - 1 else None
                bible_books = list(BibleDb.objects.values_list('tamilname', flat=True).distinct())

                # If at the last chapter, set next to first chapter of next book
                if next_chapter is None:
                    book_index = bible_books.index(current_book)
                    next_book = bible_books[book_index + 1] if book_index + 1 < len(bible_books) else None
                    if next_book:
                        next_book=next_book
                        print('next_book',next_book)
                        next_chapter = BibleDb.objects.filter(bookname=next_book).order_by('chapter').first().chapter
                        print('next_chapter',next_chapter)
            
                if prev_chapter is None:
                    book_index = bible_books.index(current_book)
                    prev_book = bible_books[book_index-1] if book_index - 1 >= 0 else None
                    if prev_book:
                        prev_book=prev_book
                        prev_book_chapters = BibleDb.objects.filter(bookname=prev_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))
                        prev_chapter=len(prev_book_chapters)
                
                return render(request, 'chapter_detail.html', {
                    'book': book,
                    'chapter': chapter,
                    'verses': verses,
                    'books': books,
                    'bookname': bookname,
                    'breadcrumbs': breadcrumbs,
                    "prev_chapter": prev_chapter,
                    "next_chapter": next_chapter,
                    #to conversion
                    # "bookname": current_book,
                    "next_book":next_book,
                    "prev_book":prev_book
                })

    # If no book is selected, render the base page with all books
    return render(request, 'base.html', {'books': books, 'breadcrumbs': breadcrumbs})


# def base(request):
#     books = BibleDb.objects.values('tamilname').distinct()
#     book = request.GET.get('book')
#     chapter = request.GET.get('chapter')
#     versecount = request.GET.get('versecount')
    
#     # Get the current verse details based on bookname, chapter, and versecount
#     current_verse = get_object_or_404(BibleDb, tamilname=book, chapter=chapter, versecount=versecount)
    
#     # Get the previous and next verses based on id
#     previous_verse = BibleDb.objects.filter(id__lt=current_verse.id,tamilname=book, chapter=chapter).order_by('-id').first() 
#     next_verse = BibleDb.objects.filter(id__gt=current_verse.id,tamilname=book, chapter=chapter).order_by('id').first()

#     breadcrumbs = [{'name': 'Home', 'url': reverse('base')}]
#     if book:
#         englishbook = BibleDb.objects.filter(tamilname=book).first()
#         bookname = englishbook.bookname if englishbook else None
#         breadcrumbs.append({'name': book, 'url': f'?book={book}'})  # Link for the selected book

#         if chapter:
#             breadcrumbs.append({'name': f'Chapter {chapter}', 'url': f'?book={book}&chapter={chapter}'})  # Link for the selected chapter

#             if versecount:
#                 breadcrumbs.append({'name': f'Verse {versecount}', 'url': f'?book={book}&chapter={chapter}&versecount={versecount}'})  # Link for the selected verse

#             verse_details = BibleDb.objects.filter(tamilname=book, chapter=chapter, versecount=versecount) if versecount else None
#             if versecount and verse_details.exists():
#                 return render(request, 'verse_detail.html', {
#                     'book': book,
#                     'bookname': bookname,
#                     'chapter': chapter,
#                     'versecount': versecount,
#                     'verse_details': verse_details,
#                     'books': books,
#                     'breadcrumbs': breadcrumbs,
#                     "previous_verse": previous_verse,
#                     "next_verse": next_verse,
#                 })
#             else:
#                 verses = BibleDb.objects.filter(tamilname=book, chapter=chapter)
#                 return render(request, 'chapter_detail.html', {
#                     'book': book,
#                     'chapter': chapter,
#                     'verses': verses,
#                     'books': books,
#                     'bookname': bookname,
#                     'breadcrumbs': breadcrumbs
#                 })

#     return render(request, 'base.html', {'books': books, 'breadcrumbs': breadcrumbs})

# def base(request):
#     books = BibleDb.objects.values('tamilname').distinct()
#     book = request.GET.get('book')
#     chapter = request.GET.get('chapter')
#     versecount = request.GET.get('versecount')

#     englishbook = BibleDb.objects.filter(tamilname=book).first()
#     bookname = englishbook.bookname

#     if book and chapter:
#         if versecount:
#             verse_details = BibleDb.objects.filter(tamilname=book, chapter=chapter, versecount=versecount)
#             if verse_details.exists():
#                 return render(request, 'verse_detail.html', {'book': book,"bookname":bookname, 'chapter': chapter,'versecount':versecount,'verse_details': verse_details, 'books': books})
#         else:
#             verses = BibleDb.objects.filter(tamilname=book, chapter=chapter)
#             return render(request, 'chapter_detail.html', {'book': book, 'chapter': chapter, 'verses': verses, 'books': books,"bookname":bookname})
#     return render(request,'base.html',{'books': books})

def base_english(request):
    books = BibleDb.objects.values('bookname').distinct()
    book = request.GET.get('book')
    chapter = request.GET.get('chapter')
    versecount = request.GET.get('versecount')
    
    # Get the current verse details based on bookname, chapter, and versecount
    current_verse = get_object_or_404(BibleDb, bookname=book, chapter=chapter, versecount=versecount)
    
    # Get the previous and next verses based on id
    previous_verse = BibleDb.objects.filter(id__lt=current_verse.id,bookname=book, chapter=chapter).order_by('-id').first() 
    next_verse = BibleDb.objects.filter(id__gt=current_verse.id,bookname=book, chapter=chapter).order_by('id').first()

    if book and chapter:
        if versecount:
            verse_details = BibleDb.objects.filter(bookname=book, chapter=chapter, versecount=versecount)
            if verse_details.exists():
                return render(request, 'verse_detailenglish.html', {'book': book, 'chapter': chapter,'versecount':versecount, 'verse_details': verse_details, 'books': books,"previous_verse": previous_verse,
                               "next_verse": next_verse,})
        else:
            verses = BibleDb.objects.filter(bookname=book, chapter=chapter)
            return render(request, 'chapter_detailenglish.html', {'book': book, 'chapter': chapter, 'verses': verses, 'books': books})
    return render(request,'base_english.html',{'books': books})

##################################################################
#    old_test=OldTestamentBook.objects.all()
#    new_test=NewTestamentBook.objects.all()
#    bookschapter=[]
#    for i in old_test:
#        bookschapter.append(i.booknametamil)
#    for j in new_test:
#        bookschapter.append(j.booknametamil)
#    return render(request,'base.html',{'bookschapter': bookschapter})

def index(request):
    # Fetch distinct book names from the database
    books = BibleDb.objects.values('tamilname').distinct()
    old_test = OldTestamentBook.objects.all()
    new_test = NewTestamentBook.objects.all()

    # Combine the lists of books from Old Testament and New Testament
    bookschapter = []
    for i in old_test:
        bookschapter.append(i.booknametamil)
    for j in new_test:
        bookschapter.append(j.booknametamil)

    # Handling POST request (Search form submission)
    if request.method == "POST":
        bookname = request.POST.get("Bookname")
        chapter = request.POST.get("Chapter")
        versecount = request.POST.get("Versecount")

        # Filter the queryset based on search criteria
        results = BibleDb.objects.filter(
            bookname=bookname,
            chapter=chapter,
            versecount=versecount
        )

        # Prepare breadcrumbs
        breadcrumbs = [
            {'name': 'Home', 'url': '/'},
            {'name': bookname, 'url': f'/tamil/{bookname}/'},  # Use bookname here
            {'name': f'Chapter {chapter}', 'url': f'/tamil/{bookname}/{chapter}/'}
        ]

        # Render the search results template if there are results
        return render(request, 'search_results.html', {
            'results': results,
            'breadcrumbs': breadcrumbs,
            'bookname': bookname,
            'chapter': chapter,
            'versecount': versecount,
            'books': books,
        })

    # If no POST request (just page load), render the search form
    book_names = BibleDb.objects.values_list('bookname', flat=True).distinct()
    return render(request, 'index.html', {
        'book_names': book_names,
        'bookschapter': bookschapter,
        'books': books
    })



from django.shortcuts import render
from .models import BibleDb

def song_list(request):
    # Retrieve distinct song names (bookname)
    songs = BibleDb.objects.values('bookname').distinct()
    chapters = None
    songname = None
    chapters = BibleDb.objects.all()
    return render(request, 'song_list.html', {'chapters': chapters})

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from tamilbible.models import BibleDb

def chapter2(request, bookname, chapter):
    #try:
        # Ensure chapter is a valid integer
    #    chapter = int(chapter)
   # except ValueError:
    #    return HttpResponseBadRequest("Invalid chapter number")

    # Get all distinct Tamil book names
    books = BibleDb.objects.values('tamilname').distinct()

    # Fetch the Tamil name for the given bookname
    tamilbook = BibleDb.objects.filter(bookname=bookname).first()
    if not tamilbook:
        return HttpResponseNotFound("Book not found")
    
    # Retrieve the Tamil name for the book
    book = tamilbook.tamilname

    # Fetch verses for the current chapter
    verses = BibleDb.objects.filter(bookname=bookname, chapter=chapter)
    
    # Determine next and previous chapters
    current_chapter_number = int(chapter)  # Extracting chapter number
    current_book = bookname
    next_book=bookname    
    prev_book=bookname
    current_chapter=chapter
 
    # Get all chapters of the current book
    all_chapters = BibleDb.objects.filter(bookname=current_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))

    # Find index of current chapter
    chapter_index = list(all_chapters).index(chapter)

    # Determine previous and next chapters
    prev_chapter = all_chapters[chapter_index - 1] if chapter_index > 0 else None
    next_chapter = all_chapters[chapter_index + 1] if chapter_index < len(all_chapters) - 1 else None
    bible_books = list(BibleDb.objects.values_list('bookname', flat=True).distinct())

    # If at the last chapter, set next to first chapter of next book
    if next_chapter is None:
        book_index = bible_books.index(current_book)
        next_book = bible_books[book_index + 1] if book_index + 1 < len(bible_books) else None
        if next_book:
            next_book=next_book
            print('next_book',next_book)
            next_chapter = BibleDb.objects.filter(bookname=next_book).order_by('chapter').first().chapter
            print('next_chapter',next_chapter)
  
    if prev_chapter is None:
        book_index = bible_books.index(current_book)
        prev_book = bible_books[book_index-1] if book_index - 1 >= 0 else None
        if prev_book:
            prev_book=prev_book
            prev_book_chapters = BibleDb.objects.filter(bookname=prev_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))
            prev_chapter=len(prev_book_chapters)
 
   # Determine the previous chapter
   # previous_chapter = chapter - 1 if chapter > 1 else None
   # previous_verses = (
   #     BibleDb.objects.filter(bookname=bookname, chapter=previous_chapter)
   #     if previous_chapter and BibleDb.objects.filter(bookname=bookname, chapter=previous_chapter).exists()
   #     else None
   # )

    # Determine the next chapter
   # next_chapter = chapter + 1 if BibleDb.objects.filter(bookname=bookname, chapter=chapter + 1).exists() else None
   # next_verses = (
   #     BibleDb.objects.filter(bookname=bookname, chapter=next_chapter)
   #     if next_chapter
   #     else None
   # )

    # Prepare the context
    context = {
        "bookname": bookname,            # English book name
        "book": book,                    # Tamil book name
        "chapter": chapter,              # Current chapter
        "verses": verses,                # Verses for the current chapter
       # "previous_chapter": previous_chapter,  # Previous chapter (if exists)
       # "previous_verses": previous_verses,    # Verses for the previous chapter
       # "next_chapter": next_chapter,          # Next chapter (if exists)
       # "next_verses": next_verses,            # Verses for the next chapter
        "books": books,                        # List of all distinct books
        "all_chapters":all_chapters,
        "prev_chapter": prev_chapter,
        "next_chapter": next_chapter,
        #to conversion
        "bookname": current_book,
        "next_book":next_book,
        "prev_book":prev_book
    }

    return render(request, 'chapter2.html', context)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from tamilbible.models import BibleDb
from django.db import models
from django.db.models.functions import Cast

def chapter_detail(request, bookname, chapter):
    books = BibleDb.objects.values('tamilname').distinct()
    
   # try:
   #    chapter = int(chapter)  # Ensure chapter is an integer
   # except ValueError:
   #     return HttpResponseBadRequest("Invalid chapter number")

    # Get the book name in Tamil
    tamilbook = BibleDb.objects.filter(bookname=bookname).first()
    if not tamilbook:
        return HttpResponseNotFound("Book not found")

    book = tamilbook.tamilname

    # Fetch current chapter verses
    verses = BibleDb.objects.filter(bookname=bookname, chapter=chapter)
    
    # Determine next and previous chapters
    current_chapter_number = int(chapter)  # Extracting chapter number
    current_book = bookname
    next_book=bookname    
    prev_book=bookname
    current_chapter=chapter
 
    # Get all chapters of the current book
    all_chapters = BibleDb.objects.filter(bookname=current_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))

    # Find index of current chapter
    chapter_index = list(all_chapters).index(chapter)
    
    # Determine previous and next chapters
    prev_chapter = all_chapters[chapter_index - 1] if chapter_index > 0 else None
    next_chapter = all_chapters[chapter_index + 1] if chapter_index < len(all_chapters) - 1 else None
    bible_books = list(BibleDb.objects.values_list('bookname', flat=True).distinct())

    # If at the last chapter, set next to first chapter of next book
    if next_chapter is None:
        book_index = bible_books.index(current_book)
        next_book = bible_books[book_index + 1] if book_index + 1 < len(bible_books) else None
        if next_book:
            next_book=next_book
            print('next_book',next_book)
            next_chapter = BibleDb.objects.filter(bookname=next_book).order_by('chapter').first().chapter
            print('next_chapter',next_chapter)
  
    if prev_chapter is None:
        book_index = bible_books.index(current_book)
        prev_book = bible_books[book_index-1] if book_index - 1 >= 0 else None
        if prev_book:
            prev_book=prev_book
            prev_book_chapters = BibleDb.objects.filter(bookname=prev_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))
            prev_chapter=len(prev_book_chapters) 
    # Fetch all chapters for navigation
   # all_chapters = (
   #     BibleDb.objects.filter(bookname=bookname)
   #     .values_list('chapter', flat=True)
   #     .distinct()
   # )

    # Prepare previous and next chapter info
   # previous_chapter_info = BibleDb.objects.filter(bookname=bookname, chapter=chapter - 1).first()
   # next_chapter_info = BibleDb.objects.filter(bookname=bookname, chapter=chapter + 1).first()

    # Prepare breadcrumbs
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Tamil Bible', 'url': '/tamil/'},
        {'name': f'{book} -  {chapter}', 'url': None},
    ]
    
    context = {
        "bookname": bookname,
        "book": book,
        "chapter": chapter,
        "verses": verses,
       # "previous_chapter_info": previous_chapter_info,
       # "next_chapter_info": next_chapter_info,
        "all_chapters": all_chapters,
        "books": books,
        "breadcrumbs": breadcrumbs,
        "prev_chapter": prev_chapter,
        "next_chapter": next_chapter,
        #to conversion
        "bookname": current_book,
        "next_book":next_book,
        "prev_book":prev_book
    }

    return render(request, 'chapter_detail.html', context)



# from django.shortcuts import render
# from django.http import HttpResponseNotFound, HttpResponseBadRequest
# from tamilbible.models import BibleDb

# def chapter_detail(request, bookname, chapter):
#     # Ensure chapter is an integer
#     try:
#         chapter = int(chapter)
#     except ValueError:
#         return HttpResponseBadRequest("Invalid chapter number")

#     # Get the Tamil name of the book (or a localized name)
#     tamilbook = BibleDb.objects.filter(bookname=bookname).first()  # Use filter to avoid MultipleObjectsReturned
#     if not tamilbook:
#         return HttpResponseNotFound("Book not found")
    
#     book = tamilbook.tamilname

#     # Fetch all chapters for the given book
#     all_chapters = BibleDb.objects.filter(bookname=bookname).values_list('chapter', flat=True).distinct()

#     # Fetch current chapter verses
#     verses = BibleDb.objects.filter(bookname=bookname, chapter=chapter)

#     # Fetch previous and next chapters and their verses
#     previous_chapter = chapter - 1 if chapter > 1 else None
#     previous_verses = BibleDb.objects.filter(bookname=bookname, chapter=previous_chapter) if previous_chapter else None

#     next_chapter = chapter + 1 if BibleDb.objects.filter(bookname=bookname, chapter=chapter + 1).exists() else None
#     next_verses = BibleDb.objects.filter(bookname=bookname, chapter=next_chapter) if next_chapter else None

#     # Fetch list of distinct books for the sidebar or dropdown
#     books = BibleDb.objects.values('tamilname').distinct()

#     # Prepare breadcrumbs
#     breadcrumbs = [
#         {'name': 'Home', 'url': '/'},
#         {'name': book, 'url': f'/tamil/{bookname}/'},
#         {'name': f'Chapter {chapter}', 'url': f'/tamil/{bookname}/{chapter}/'}
#     ]

#     # Prepare context for the template
#     context = {
#         "bookname": bookname,
#         "book": book,
#         "chapter": chapter,
#         "verses": verses,
#         "previous_chapter": previous_chapter,
#         "previous_verses": previous_verses,
#         "next_chapter": next_chapter,
#         "next_verses": next_verses,
#         "books": books,
#         "breadcrumbs": breadcrumbs,
#         "all_chapters": all_chapters,  # Send all chapters to the template
#     }

#     return render(request, 'chapter_detail.html', context)

# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponseNotFound, HttpResponseBadRequest
# from tamilbible.models import BibleDb

# def chapter_detail(request, bookname, chapter):
#     books = BibleDb.objects.values('tamilname').distinct()
#     try:
#         chapter = int(chapter)  # Ensure chapter is an integer
#     except ValueError:
#         return HttpResponseBadRequest("Invalid chapter number")

#     # Get the book name in Tamil (or a localized name)
#     tamilbook = BibleDb.objects.filter(bookname=bookname).first()
#     if not tamilbook:
#         return HttpResponseNotFound("Book not found")
    
#     book = tamilbook.tamilname

#     # Fetch current chapter verses
#     verses = BibleDb.objects.filter(bookname=bookname, chapter=chapter)

#     # Fetch previous and next chapters and their verses
#     previous_chapter = chapter - 1 if chapter > 1 else None
#     previous_verses = (
#         BibleDb.objects.filter(bookname=bookname, chapter=previous_chapter)
#         if previous_chapter and BibleDb.objects.filter(bookname=bookname, chapter=previous_chapter).exists()
#         else None
#     )

#     next_chapter = chapter + 1 if BibleDb.objects.filter(bookname=bookname, chapter=chapter + 1).exists() else None
#     next_verses = (
#         BibleDb.objects.filter(bookname=bookname, chapter=next_chapter)
#         if next_chapter
#         else None
#     )
#     # Prepare breadcrumbs
#     breadcrumbs = [
#         {'name': 'Home', 'url': '/'},
#         {'name': book, 'url': f'/tamil/{bookname}/'},
#         {'name': f'Chapter {chapter}', 'url': f'/tamil/{bookname}/{chapter}/'}
#     ]
#     # Prepare context for the template
#     context = {
#         "bookname": bookname,
#         "book": book,
#         "chapter": chapter,
#         "verses": verses,
#         "previous_chapter": previous_chapter,
#         "previous_verses": previous_verses,
#         "next_chapter": next_chapter,
#         "next_verses": next_verses,
#         "books":books,
#         "breadcrumbs": breadcrumbs,
#     }

#     return render(request, 'chapter_detail.html', context)

# def chapter_detail_english(request,bookname,chapter):
#     books = BibleDb.objects.values('bookname').distinct()
#     book=bookname
#     chapter=chapter
#     # Get the verses related to the selected chapter
#     verses = BibleDb.objects.filter(bookname=bookname,chapter=chapter)
#     # Breadcrumbs logic
#     breadcrumbs = [
#         {'name': 'Home', 'url': '/'},  # Link to the home page
#         {'name': 'Books List (English)', 'url': '/books/english/'},  # Link to the book list page
#         {'name': bookname, 'url': f'/bible/{bookname}/'},  # Link to the book page
#         {'name': f'Chapter {chapter}', 'url': f'/bible/{bookname}/{chapter}/'}  # Link to the specific chapter
#     ]
#     return render(request, 'chapter_detailenglish.html', {"breadcrumbs":breadcrumbs,"verses":verses,"books":books,"book":book,"chapter":chapter})

def chapter_detail_english(request, bookname, chapter):
    books = BibleDb.objects.values('bookname').distinct()
    book = bookname

    # Ensure chapter is converted to an integer
   # try:
   #     chapter = int(chapter)
   # except ValueError:
   #     return HttpResponse("Invalid chapter number.", status=400)

    # Get the verses related to the selected chapter
    verses = BibleDb.objects.filter(bookname=bookname, chapter=chapter)

    # Fetch all chapters for the given book
   # all_chapters = BibleDb.objects.filter(bookname=bookname).values_list('chapter', flat=True).distinct()

    # Fetch previous and next chapters
   # previous_chapter = chapter - 1 if chapter > 1 else None
   # next_chapter = chapter + 1 if BibleDb.objects.filter(bookname=bookname, chapter=chapter + 1).exists() else None

    # Breadcrumbs logic
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Bible', 'url': '/english/'},
        {'name': f'{bookname.capitalize()}  {chapter}', 'url': None},
    ]

    # Determine next and previous chapters
    
    current_book = bookname
    next_book=bookname    
    prev_book=bookname
    
 
    # Get all chapters of the current book
    all_chapters = BibleDb.objects.filter(bookname=current_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))

    # Find index of current chapter
    chapter_index = list(all_chapters).index(chapter)
    
    # Determine previous and next chapters
    prev_chapter = all_chapters[chapter_index - 1] if chapter_index > 0 else None
    next_chapter = all_chapters[chapter_index + 1] if chapter_index < len(all_chapters) - 1 else None
    bible_books = list(BibleDb.objects.values_list('bookname', flat=True).distinct())

    # If at the last chapter, set next to first chapter of next book
    if next_chapter is None:
        book_index = bible_books.index(current_book)
        next_book = bible_books[book_index + 1] if book_index + 1 < len(bible_books) else None
        if next_book:
            next_book=next_book
            next_chapter = BibleDb.objects.filter(bookname=next_book).order_by('chapter').first().chapter
            
  
    if prev_chapter is None:
        book_index = bible_books.index(current_book)
        prev_book = bible_books[book_index-1] if book_index - 1 >= 0 else None
        if prev_book:
            prev_book=prev_book
            prev_book_chapters = BibleDb.objects.filter(bookname=prev_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))
            prev_chapter=len(prev_book_chapters)

    return render(request, 'chapter_detailenglish.html', {
       # "next_chapter_info": {"bookname": bookname, "chapter": next_chapter} if next_chapter else None,
       # "previous_chapter_info": {"bookname": bookname, "chapter": previous_chapter} if previous_chapter else None,
        "all_chapters": all_chapters,
        "breadcrumbs": breadcrumbs,
        "verses": verses,
        "books": books,
        "book": book,
        "chapter": chapter,
        "prev_chapter": prev_chapter,
        "next_chapter": next_chapter,
        #to conversion
        "bookname": current_book,
        "next_book":next_book,
        "prev_book":prev_book
    })



from django.shortcuts import render, get_object_or_404
from .models import BibleDb

def chapter3(request, bookname, chapter):
    # Get distinct book names
    books = BibleDb.objects.values('bookname').distinct()

    # Validate and retrieve verses
    #try:
    #    chapter = int(chapter)
    #    verses = BibleDb.objects.filter(bookname=bookname, chapter=chapter)
    #except ValueError:
    #    verses = None

    # Handle the case where no verses exist
    #if not verses.exists():
    #    error_message = f"No verses found for {bookname} chapter {chapter}."
    #    return render(request, 'chapter3.html', {
    #        "error_message": error_message,
    #        "books": books,
    #        "book": bookname,
    #        "chapter": chapter
    #    })

    verses = BibleDb.objects.filter(bookname=bookname, chapter=chapter)
    
    # Determine next and previous chapters
    
    current_book = bookname
    next_book=bookname    
    prev_book=bookname
    
 
    # Get all chapters of the current book
    all_chapters = BibleDb.objects.filter(bookname=current_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))

    # Find index of current chapter
    chapter_index = list(all_chapters).index(chapter)
    
    # Determine previous and next chapters
    prev_chapter = all_chapters[chapter_index - 1] if chapter_index > 0 else None
    next_chapter = all_chapters[chapter_index + 1] if chapter_index < len(all_chapters) - 1 else None
    bible_books = list(BibleDb.objects.values_list('bookname', flat=True).distinct())

    # If at the last chapter, set next to first chapter of next book
    if next_chapter is None:
        book_index = bible_books.index(current_book)
        next_book = bible_books[book_index + 1] if book_index + 1 < len(bible_books) else None
        if next_book:
            next_book=next_book
            next_chapter = BibleDb.objects.filter(bookname=next_book).order_by('chapter').first().chapter
            
  
    if prev_chapter is None:
        book_index = bible_books.index(current_book)
        prev_book = bible_books[book_index-1] if book_index - 1 >= 0 else None
        if prev_book:
            prev_book=prev_book
            prev_book_chapters = BibleDb.objects.filter(bookname=prev_book).values_list('chapter', flat=True).distinct().order_by(Cast('chapter', output_field=models.IntegerField()))
            prev_chapter=len(prev_book_chapters)

    return render(request, 'chapter3.html', {
        "verses": verses,
        "books": books,
        "book": bookname,
        "chapter": chapter,
        "all_chapters": all_chapters,
        "prev_chapter": prev_chapter,
        "next_chapter": next_chapter,
        #to conversion
        "bookname": current_book,
        "next_book":next_book,
        "prev_book":prev_book
    })


# def chapter3(request,bookname,chapter):
#     books = BibleDb.objects.values('bookname').distinct()
#     book=bookname
#     chapter=chapter
#     # Get the verses related to the selected chapter
#     verses = BibleDb.objects.filter(bookname=bookname,chapter=chapter)
#     return render(request, 'chapter3.html', {"verses":verses,"books":books,"book":book,"chapter":chapter})


from django.shortcuts import render
from .models import BibleDb  # Replace with your actual model

def verse_details(request, verse_count):
    # Use filter to get all records that match verse_count
    verses = BibleDb.objects.filter(versecount=verse_count)
    
    # Prepare breadcrumbs
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Bible Verses', 'url': '/verses/'},  # Adjust the URL to your verse list page
        {'name': f'Verse {verse_count}', 'url': f'/verses/{verse_count}/'}
    ]
    
    # If there's only one result, render it directly
    if verses.count() == 1:
        verse = verses.first()
        return render(request, 'verse_details.html', {'verse': verse, 'breadcrumbs': breadcrumbs})
    else:
        # If there are multiple results, show the list
        return render(request, 'verse_details.html', {'verses': verses, 'breadcrumbs': breadcrumbs})


# from django.shortcuts import render
# from .models import BibleDb  # Replace with your actual model

# def verse_details(request, verse_count):
#     # Use filter to get all records that match verse_count
#     verses = BibleDb.objects.filter(versecount=verse_count)
    
#     if verses.count() == 1:
#         # If there is exactly one result, return it
#         verse = verses.first()
#         return render(request, 'verse_details.html', {'verse': verse})
#     else:
#         # Handle multiple results (e.g., show a list or return an error message)
    
#         return render(request, 'verse_details.html', {'verses': verses})


def verse(request,bookname,chapter,versecount):
    print("INSIDE VERRRR DETAILSSSS 222")
    books = BibleDb.objects.values('tamilname').distinct()
    tamilbook=BibleDb.objects.filter(bookname=bookname).first()
    book=tamilbook.tamilname
    chapter=chapter
    versecount=versecount
    # Get the specific verse details
    verse_details = BibleDb.objects.filter(bookname=bookname, chapter=chapter, versecount=versecount)
    old_test=OldTestamentBook.objects.all()
    new_test=NewTestamentBook.objects.all()
    bookschapter=[]
    for i in old_test:
        bookschapter.append(i.booknametamil)
    for j in new_test:
        bookschapter.append(j.booknametamil)
    return render(request, 'verse.html', {"verse_details":verse_details,"bookschapter":bookschapter,'books':books,"book":book,"chapter":chapter,"versecount":versecount})


from django.shortcuts import render, get_object_or_404
from .models import BibleDb

def verse_detail(request,bookname,chapter,versecount):
    print("INSIDE VERRRR DETAILSSSS BOOKNAME")
    books = BibleDb.objects.values('tamilname').distinct()
    tamilbook=BibleDb.objects.filter(bookname=bookname).first()
    book=tamilbook.tamilname
    bookname=bookname
    chapter=chapter
    versecount=versecount

    # Get the current verse details based on bookname, chapter, and versecount
    current_verse = get_object_or_404(BibleDb, bookname=bookname, chapter=chapter, versecount=versecount)
    
    # Get the previous and next verses based on id
    previous_verse = BibleDb.objects.filter(id__lt=current_verse.id,bookname=bookname, chapter=chapter).order_by('-id').first()
    next_verse = BibleDb.objects.filter(id__gt=current_verse.id,bookname=bookname, chapter=chapter).order_by('id').first()

    # Get the specific verse details
    verse_details = BibleDb.objects.filter(bookname=bookname, chapter=chapter, versecount=versecount)
    old_test=OldTestamentBook.objects.all()
    new_test=NewTestamentBook.objects.all()
    bookschapter=[]
    for i in old_test:
        bookschapter.append(i.booknametamil)
    for j in new_test:
        bookschapter.append(j.booknametamil)
    # Prepare breadcrumbs
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
         {'name': 'Tamil Bible', 'url': '/tamil/'},
         {'name': f'{book}  {chapter}', 'url': f'/tamil/{book}/{chapter}/'},
         {'name': f'{book}{chapter}:{versecount}', 'url': None},  # Final breadcrumb
    ]
    return render(request, 'verse_detail.html', {"breadcrumbs":breadcrumbs,"verse_details":verse_details,"bookschapter":bookschapter,'books':books,"book":book,"bookname":bookname,"chapter":chapter,"versecount":versecount,"previous_verse": previous_verse,"next_verse": next_verse,})

def verse_detail2(request, bookname, chapter, versecount):
    print('test')    # Get the Tamil book name for display
    tamilbook = BibleDb.objects.filter(bookname=bookname).first()
    book = tamilbook.tamilname
    bookname = bookname
    chapter = chapter
    versecount = versecount  # Ensure versecount is treated as an integer

    # Get the current verse details based on bookname, chapter, and versecount
    current_verse = get_object_or_404(BibleDb, bookname=bookname, chapter=chapter, versecount=versecount)
    
    # Get the previous and next verses based on id
    previous_verse = BibleDb.objects.filter(id__lt=current_verse.id,bookname=bookname, chapter=chapter).order_by('-id').first() 
    next_verse = BibleDb.objects.filter(id__gt=current_verse.id,bookname=bookname, chapter=chapter).order_by('id').first()

    # Get the list of books for chapter navigation
    old_test = OldTestamentBook.objects.all()
    new_test = NewTestamentBook.objects.all()
    bookschapter = [i.booknametamil for i in old_test] + [j.booknametamil for j in new_test]

    # Fetch verse details for the current verse
    verse_details = BibleDb.objects.filter(bookname=bookname, chapter=chapter, versecount=versecount)

    return render(request, 'verse_detail2.html', {
        "verse_details": verse_details,
        "bookschapter": bookschapter,
        'books': BibleDb.objects.values('tamilname').distinct(),
        "book": book,
        "bookname": bookname,
        "chapter": chapter,
        "versecount": versecount,
        "previous_verse": previous_verse,
        "next_verse": next_verse,
    })

def verse_detail3(request, bookname, chapter, versecount):
    print('test3')    # Get the Tamil book name for display
    tamilbook = BibleDb.objects.filter(bookname=bookname).first()
    book = tamilbook.tamilname
    bookname = bookname
    chapter = chapter
    versecount = versecount  # Ensure versecount is treated as an integer

    # Get the current verse details based on bookname, chapter, and versecount
    current_verse = get_object_or_404(BibleDb, bookname=bookname, chapter=chapter, versecount=versecount)
    
    # Get the previous and next verses based on id
    previous_verse = BibleDb.objects.filter(id__lt=current_verse.id,bookname=bookname, chapter=chapter).order_by('-id').first() 
    next_verse = BibleDb.objects.filter(id__gt=current_verse.id,bookname=bookname, chapter=chapter).order_by('id').first()

    # Get the list of books for chapter navigation
    old_test = OldTestamentBook.objects.all()
    new_test = NewTestamentBook.objects.all()
    bookschapter = [i.booknametamil for i in old_test] + [j.booknametamil for j in new_test]

    # Fetch verse details for the current verse
    verse_details = BibleDb.objects.filter(bookname=bookname, chapter=chapter, versecount=versecount)

    return render(request, 'verse_detail3.html', {
        "verse_details": verse_details,
        "bookschapter": bookschapter,
        'books': BibleDb.objects.values('bookname').distinct(),
        "book": book,
        "bookname": bookname,
        "chapter": chapter,
        "versecount": versecount,
        "previous_verse": previous_verse,
        "next_verse": next_verse,
    })


# def verse_detail_english(request,bookname,chapter,versecount):
#     books = BibleDb.objects.values('bookname').distinct()
    
#     tamilname=BibleDb.objects.filter(bookname=bookname).first()
#     tamilbook=tamilname.tamilname

#     book=bookname
#     chapter=chapter
#     versecount=versecount
#     verse_details = BibleDb.objects.filter(bookname=bookname, chapter=chapter, versecount=versecount)
#     return render(request, 'verse_detailenglish.html', {"verse_details":verse_details,"books":books,"book":book,"tamilbook":tamilbook,"chapter":chapter,"versecount":versecount})

from django.shortcuts import render
from .models import BibleDb

def verse_detail_english(request, bookname, chapter, versecount):
    # Fetch distinct book names from the database
    books = BibleDb.objects.values('bookname').distinct()

    # Get the Tamil name of the book
    tamilname = BibleDb.objects.filter(bookname=bookname).first()
    tamilbook = tamilname.tamilname

    # Define variables
    book = bookname
    chapter = chapter
    versecount = versecount

    # Get the specific verse details
    verse_details = BibleDb.objects.filter(bookname=bookname, chapter=chapter, versecount=versecount)
    
    # Get the current verse details based on bookname, chapter, and versecount
    current_verse = get_object_or_404(BibleDb, bookname=bookname, chapter=chapter, versecount=versecount)
    
    # Get the previous and next verses based on id
    previous_verse = BibleDb.objects.filter(id__lt=current_verse.id,bookname=bookname, chapter=chapter).order_by('-id').first()
    next_verse = BibleDb.objects.filter(id__gt=current_verse.id,bookname=bookname, chapter=chapter).order_by('id').first()
    
    # Breadcrumbs logic
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
         {'name': 'Bible', 'url': '/tamil/'},
         {'name': f'{bookname.capitalize()}  {chapter}', 'url': f'/english/{bookname}/{chapter}/'},
         {'name': f'{bookname.capitalize()}{chapter}:{versecount}', 'url': None},  # Final breadcrumb
    ]

    # Pass breadcrumbs and other context variables to the template
    return render(request, 'verse_detailenglish.html', {
        'verse_details': verse_details,
        'books': books,
        'book': book,
        'tamilbook': tamilbook,
        'chapter': chapter,
        'versecount': versecount,
        "previous_verse": previous_verse,
                   "next_verse": next_verse,
        'breadcrumbs': breadcrumbs  # Pass breadcrumbs to the template
    })
