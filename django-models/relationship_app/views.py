from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book 
from .models import Library
from .forms import CreateUserForm, LoginForm

# authentication models and functions
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

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
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            # authenticate users
            user = authenticate(username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('books/')
    
    context = {'form':form}


    return render(request, 'relationship_app/login.html', context=context)

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        
    context = {'form': form}

    return render(request, 'relationship_app/register.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('login')