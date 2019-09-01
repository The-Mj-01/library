from django.urls import path , re_path
from . import views


app_name = 'book'
urlpatterns = [
    path('', views.index , name = 'index'),
    path('list', views.BookListView.as_view() , name='bookList'),
    path('borrows', views.AllBorrowedListView.as_view() , name='allBorrowed'),
    path('mybooks' , views.LoanedBookByUserListView.as_view() , name='mybooks'),
    path('detail/<uuid:pk>/renew' , views.renew_book_librarian , name = 'renewBookLibrarian'),
    # path('detail/<int:pk>', views.BookDetailView.as_view() , name= 'bookDetail'),
    re_path(r'^detail/(?P<pk>\d+)$', views.BookDetailView.as_view() , name= 'bookDetail'),
    re_path(r'^get$', views.APIListCreateBook.as_view() , name= 'apiBookList'),
    re_path(r'^update/(?P<pk>\d+)$', views.APIRetrieveUpdateDestroy.as_view() , name= 'apiBookList'),
    # re_path(r'^detail/(?P<uid>[-\w]+)$')
]