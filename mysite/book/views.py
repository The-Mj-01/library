from django.shortcuts import render , get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from django.views import generic


from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

from rest_framework import generics

# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .serializers import BookSerializer

from .models import Author
from .models import BookInstance
from .models import Book
from .models import Genre

from .forms import RenewBookForm


# Create your views here.

# def email_check(user):
#     return user.email.endwith('@example.com')

@login_required
# @user_passes_test(email_check)
# @permission_required('book.can_read_private_section')
# @permission_required('book.user_watcher')
def index(request):

    # user.hasperm('user.can_add')

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    num_author = Author.objects.count()
    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_author' : num_author,
    }
    # if request.user.is_authenticated:
    return render(request , 'book/index.html' , context)
    # else:
    #     return render(request , 'book/login.html' , context)

    # if not request.user.email.endwith('@example.com'):
    #     return render(request, 'book/index.html', context)
    # else:
    #     return render(request, 'book/index.html', context)


class BookListView(LoginRequiredMixin , generic.ListView):
    model = Book
    # context_object_name = 'my_book_list'
    # template_name = 'book/book_list.html'
    # queryset = Book.objects.filter(title__icontains = 'python')[:5]
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains = 'python')[:5]
    #
    # def get_context_data(self,**kwargs):
    #     context = super(BookListView , self).get_context_data(**kwargs)
    #
    #     context['my_book_list'] = Book.objects.all()
    #     return context
    paginate_by = 2
    # permission_required = 'book.can_read_priavte_section'
    # permission_required = 'book.user_watcher'
    # permission_required = 'user.can_edit'

    def test_func(self):
        return user.email.endwith('@example.com')

    # login_url = 'accounts/login/'
    # redirect_field_name = '/'

class BookDetailView(generic.DetailView):
    model = Book


class LoanedBookByUserListView(LoginRequiredMixin , generic.ListView):
    model = BookInstance
    template_name = 'book/bookinstance_list_borrower_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o').order_by('due_back')



# def book_detail_view(request , pk):
#     try:
#         book_id = Book.objects.get( pk = pk)
#     except Book.DoesNotExist:
#         raise Http404("book does not exist.")
#
#     #book_id = get.object_or_404(Book , pk = pk)
#
#     return render(
#         request,
#         'book/book_detail.html',
#         context={'book': book_id}
#     )


class AllBorrowedListView(generic.ListView):
    model = BookInstance
    template_name = 'book/book_borrows.html'
    paginate_by = 5


@login_required
@permission_required('book.librarian')
def renew_book_librarian(request , pk):
    book_inst = get_object_or_404(BookInstance , pk = pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('book:allBorrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta (weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})

    context = {
        'form': form,
        'book_inst' : book_inst
    }
    return render(
        request,
        'book/book_renew_librarian.html',
        context
        )



class APIListCreateBook(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class APIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# class APIListCreateBook(APIView):
#     def get(self , request , format = None):
#         books = Book.objects.all()
#         serializer = BookSerializer(books , many=True)
#         return Response(serializer.data)
#
#     def post(self , request , format = None):
#         serializers = BookSerializer(data=request.data)
#         serialaizers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data , status=status.HTTP_201_CREATED)