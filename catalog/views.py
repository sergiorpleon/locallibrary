from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        dict(num_books=num_books,num_instances=num_instances,num_instances_available=num_instances_available,num_authors=num_authors, num_visits=num_visits),
    )
    
    
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    def get_queryset(self):
        return Book.objects.filter(title__icontains=' ')[:5] # Get 5 books containing the title war
    
    template_name = 'book_list.html'  # Specify your own template name/location
    
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'  # Specify your own template name/location
    
def book_detail_view(request,pk):
    try:
        book_id=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
        
    #book_id=get_object_or_404(Book, pk=pk)
    
    return render(
        request,
        'book_detail.html',
        context={'book':book_id,}
    )    
    
    
""" Author"""    
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    
    #queryset = Autor.objects.filter(first_name__icontains='war')[:5] # Get 5 books containing the title war
    def get_queryset(self):
        return Author.objects.filter(first_name__icontains='')[:5] # Get 5 books containing the title war
    
    template_name = 'author_list.html'  # Specify your own template name/location
    
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'  # Specify your own template name/location
    
def Author_detail_view(request,pk):
    try:
        book_id=Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        raise Http404("Author does not exist")
        
    #book_id=get_object_or_404(Autor, pk=pk)
    
    return render(
        request,
        'author_detail.html',
        context={'author':author_id,}
    ) 
    
    
    
    
    
    
#from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(generic.ListView,):
    """
    Generic class-based view listing books on loan to current user. 
    """
    
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    
    model = BookInstance
    template_name ='bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedAllBooksListView(generic.ListView,):
    """
    Generic class-based view listing books on loan to current user. 
    """
    
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    
    model = BookInstance
    template_name ='bookinstance_list_all_borrowed.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')



"""FORM"""
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    
    
    
"""GENERIC FORM VIEW"""
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}
    template_name ='author_form.html'
    

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    template_name ='author_form.html'
    
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name ='author_confirm_delete.html'
    
    
    
    
class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    #initial={'date_of_death':'05/01/2018',}
    template_name ='book_form.html'
    

class BookUpdate(UpdateView):
    model = Book
    fields = ['title','author','summary','isbn', 'genre']
    template_name ='book_form.html'
    
class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    template_name ='book_confirm_delete.html'