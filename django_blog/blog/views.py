from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Post

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')


def home(request):
    return render(request, 'home.html')

@login_required
def posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts.html', {'posts': posts})