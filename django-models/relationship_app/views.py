from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book 
from .models import Library
from .forms import CreateUserForm, LoginForm

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# authentication models and functions
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

# importing modules for creating profile models
from django.contrib.auth.decorators import login_required

# using the user passes test decorators
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required


# Create your views here.
@permission_required('relationship_app.can_view_book', raise_exception=True)
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
        forms = UserCreationForm()

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        
    context = {'form': form}

    return render(request, 'relationship_app/register.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('login')


# creating profile views 

@login_required
def profile(request):
    return render(request, 'relationship_app/profile.html')




# Check if the user is an Admin
def Admin(user):
    return user.userprofile.role == 'Admin'

# Check if the user is a Librarian
def Librarian(user):
    return user.userprofile.role == 'Librarian'

# Check if the user is a Member
def Member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(Admin)
def Admin(request):
    return render(request, 'admin.html')  # Replace with your actual template

@user_passes_test(Librarian)
def Librarian(request):
    return render(request, 'librarian.html')  # Replace with your actual template

@user_passes_test(Member)
def Member(request):
    return render(request, 'member.html')  # Replace with your actual template