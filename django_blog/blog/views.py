from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from .forms import PostForm

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
# def posts(request):
#     posts = Post.objects.all().order_by('-created_at')
#     return render(request, 'post_list.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/post_list.html'
#     context_object_name = 'posts'
#     ordering = ['-created_at']
#     paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        context['tags'] = self.object.tags.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, author=request.user, post=self.object)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comments'] = self.object.comments.all()
#         context['comment_form'] = CommentForm()
#         return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs
    

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    


# comment view to handle comment creation
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
# Search functionality
class PostSearchView(ListView):
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
    


# post by taglist
class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # You can reuse your existing post list template
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags=tag).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return context