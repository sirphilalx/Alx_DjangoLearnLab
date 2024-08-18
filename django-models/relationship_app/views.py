from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book 
from .models import Library


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
    

# def login(request):
#     return render(request, 'relationship_app/login.html')

# def register(request):
#     form = CreateUserForm()
#     if request.method == 'POST':

#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             redirect('login')
#     return render(request, 'relationship_app/register.html')

# def logout(request):
#     return render(request, 'relationship_app/logout.html')

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'



from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # This view can only be accessed by authenticated users
    return render(request, 'profile.html')
