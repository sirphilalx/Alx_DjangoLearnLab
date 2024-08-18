from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book 
from .models import Library
from . forms import CreateUserForm 


# Create your views here.
def list_books(request):
    books = Book.objects.all()

    context = {
        'books': books
    }

    # return render(request, 'list_books.html', context)
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the list of books to the context
        context['books'] = self.object.books.all()
        return context
    

def login(request):
    return render(request, 'relationship_app/login.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('login')
    return render(request, 'relationship_app/register.html')

def logout(request):
    return render(request, 'relationship_app/logout.html')
